import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, DetailView, ListView, FormView, RedirectView
from django.template import loader, Context
from django.contrib.staticfiles import finders
from django.contrib import messages

from cartvine.utils import get_namedtuple_choices
from cartvine.apps.shop.models import Shop

from cartvine.apps.widget.models import Widget, WidgetShop
from cartvine.apps.widget.forms import FacebookAuthWidgetForm, ProductsLikeWidgetForm, ShopPropsWidgetConfigForm


class AvailableWidgetView(ListView):
    model = Widget

    def get_queryset(self):
        shop = Shop.objects.filter(users__in=[self.request.user])
        return Widget.objects.exclude(shop=shop).all()


class MyWidgetView(ListView):
    model = Widget

    def get_queryset(self):
        self.shop = Shop.objects.filter(users__in=[self.request.user])
        return Widget.objects.filter(shop=self.shop)

    def get_context_data(self, **kwargs):
        context = super(MyWidgetView, self).get_context_data(**kwargs)
        context['available_widgets'] = Widget.objects.filter(is_active=True)
        return context


class WidgetInfoView(DetailView):
    model = Widget
    slug_field = 'slug'


class MyWidgetEditView(FormView):
    WIDGET_FORMS = get_namedtuple_choices('WIDGET_FORMS', (
        (FacebookAuthWidgetForm, 'widget_auth_facebook', 'Facebook Auth'),
        (ProductsLikeWidgetForm, 'widget_products_like', 'Products Like This One'),
        (ShopPropsWidgetConfigForm, 'widget_prop_plus', 'Shop Props'),
    ))
    template_name = 'widget/widget_edit.html'

    def get_form_class(self):
        form_type = self.kwargs['slug'].replace('-', '_')
        return self.WIDGET_FORMS.get_value_by_name(form_type)

    def get_success_url(self):
        return reverse('widget:edit', kwargs={'slug': self.kwargs['slug']})

    def get_initial(self):
        self.shop = Shop.objects.filter(users__in=[self.request.user])
        self.widget_config = get_object_or_404(WidgetShop.objects.filter(shop=self.shop), widget__slug=self.kwargs['slug'])
        return self.widget_config.data

    def get_context_data(self, **kwargs):
        context = super(MyWidgetEditView, self).get_context_data(**kwargs)
        context['shop'] = self.shop
        context['widget'] = get_object_or_404(Widget, slug=self.kwargs['slug'])
        context['widget_config'] = self.widget_config

        if hasattr(context['form'], 'template_name'):
            self.template_name = context['form'].template_name

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        if form.is_valid():
            if not type(self.widget_config.data).__name__ == 'dict':
                self.widget_config.data = {}

            for field in form.fields:
                self.widget_config.data[field] = form.cleaned_data[field]
            self.widget_config.save()
            messages.success(request, _('Successfully updated Widget'))

        return super(MyWidgetEditView, self).post(request, *args, **kwargs)


class WidgetLoaderView(TemplateView):
    template_name = 'widget/cartvine-loader.js'


class WidgetsForShopView(DetailView):
    """ View generates javascript response that is used to load widget js files 
    should be public 

    # compressor setup
    rm /tmp/cartvine-complete.js
    cat ~/Projects/Personal/cartvine/cartvine/apps/default/static/emberjs/js/libs/ember-0.9.8.1.min.js  >> /tmp/cartvine-complete.js
    java -jar build/yuicompressor-2.4.7.jar --charset utf-8  ~/Projects/Personal/cartvine/cartvine/apps/default/static/emberjs/js/libs/ember-routemanager.min.js >> /tmp/cartvine-complete.js
    java -jar build/yuicompressor-2.4.7.jar --charset utf-8  ~/Projects/Personal/cartvine/cartvine/apps/default/static/emberjs/js/libs/ember-data-latest.js >> /tmp/cartvine-complete.js
    java -jar build/yuicompressor-2.4.7.jar --charset utf-8  ~/Projects/Personal/cartvine/cartvine/apps/default/static/emberjs/js/libs/tastypie_adapter.js >> /tmp/cartvine-complete.js
    java -jar build/yuicompressor-2.4.7.jar --charset utf-8  ~/Projects/Personal/cartvine/cartvine/apps/default/static/emberjs/js/libs/ember-facebook.js >> /tmp/cartvine-complete.js
    """
    model = Shop
    template_name = 'widget/for_shop.js'

    def get_context_data(self, **kwargs):
        context = super(WidgetsForShopView, self).get_context_data(**kwargs)

        static_url = self.request.build_absolute_uri(settings.STATIC_URL)

        default_scripts = [
            # combined js files using yui compressor
            '%semberjs/js/ember-complete.js'%(static_url),
            '%shandlebars.js'%(static_url),
            # '%semberjs/js/libs/ember-0.9.8.1.min.js'%(static_url),
            # '%semberjs/js/libs/ember-routemanager.min.js'%(static_url),
            # '%semberjs/js/libs/ember-data-latest.js'%(static_url),
            # '%semberjs/js/libs/tastypie_adapter.js'%(static_url),
            #'%semberjs/js/libs/ember-facebook.js'%(static_url),
            #'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.13/jquery-ui.min.js',
        ]

        widget_list = Widget.objects.filter(shop=self.object)
        context['widget_list_init_names'] = [ w.widget_js_name for w in widget_list]

        context['scripts'] = default_scripts #+ [ '%s'%(self.request.build_absolute_uri(reverse('widget:script', kwargs={'shop_slug': self.object.slug, 'slug': widget.slug})),) for widget in widget_list ]

        # must be the last in this view as it needs a full context
        c = Context(context)
        templates = []
        combined_widgets = []

        for widget in widget_list:
            c['widget'] = widget
            widget_shop_join = get_object_or_404(WidgetShop, widget=widget, shop=self.object)
            c['config'] = widget_shop_join.data

            template = '%s%s.js' %('widget/', widget.slug,)
            combined_widgets.append(loader.get_template(template).render(c))

            if 'templates' in widget.data and len(widget.data['templates']) > 0:
                for template in widget.data['templates']:
                    templates.append(loader.get_template(template).render(c))

        context['templates'] = templates
        context['combined_widgets'] = ''.join(combined_widgets)

        return context


class BuyWidgetView(DetailView):
    """ View to allow widgets to be purchased 
    @TODO apply groups logic here as decorator to ensure correct widgets 
    have corect user group memberships gold/silver/bronze @TBD AH"""
    model = Widget

    def get_queryset(self):
        self.shop = Shop.objects.filter(users__in=[self.request.user])[0]
        return super(BuyWidgetView, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(BuyWidgetView, self).get_context_data(**kwargs)

        # @TODO make this pretty and safe
        if self.request.is_ajax:
            join, is_new = WidgetShop.objects.get_or_create(widget=self.object, shop=self.shop)

        return context

