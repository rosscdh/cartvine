import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, DetailView, ListView, FormView, RedirectView
from django.template import loader, Context
from django.contrib.staticfiles import finders

from cartvine.utils import get_namedtuple_choices
from cartvine.apps.shop.models import Shop

from cartvine.apps.widget.models import Widget, WidgetShop
from cartvine.apps.widget.forms import FacebookAuthWidgetForm, ProductsLikeWidgetForm, ShopPropsWidgetForm


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
        context['available_widgets'] = Widget.objects.all()
        return context


class WidgetInfoView(DetailView):
    model = Widget
    slug_field = 'slug'


class MyWidgetEditView(FormView):
    WIDGET_FORMS = get_namedtuple_choices('WIDGET_FORMS', (
        (FacebookAuthWidgetForm, 'widget_auth_facebook', 'Facebook Auth'),
        (ProductsLikeWidgetForm, 'widget_products_like', 'Products Like This One'),
        (ShopPropsWidgetForm, 'app_shop_prop', 'Shop Props'),
    ))
    template_name = 'widget/widget_edit.html'

    def get_form_class(self):
        form_type = self.kwargs['slug'].replace('-', '_')
        return self.WIDGET_FORMS.get_value_by_name(form_type)

    def get_success_url(self):
        return reverse('widget:edit', kwargs={'slug': self.kwargs['slug']})

    def get_initial(self):
        shop = Shop.objects.filter(users__in=[self.request.user])
        self.widget_config = get_object_or_404(WidgetShop.objects.filter(shop=shop), widget__slug=self.kwargs['slug'])
        return self.widget_config.data

    def get_context_data(self, **kwargs):
        context = super(MyWidgetEditView, self).get_context_data(**kwargs)
        context['widget'] = get_object_or_404(Widget, slug=self.kwargs['slug'])
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        if form.is_valid():
            if not type(self.widget_config.data).__name__ == 'dict':
                self.widget_config.data = {}

            for field in form.fields:
                self.widget_config.data[field] = form.cleaned_data[field]
            self.widget_config.save()
        return super(MyWidgetEditView, self).post(request, *args, **kwargs)


class WidgetLoaderView(TemplateView):
    template_name = 'widget/cartvine-loader.js'


class WidgetsForShopView(DetailView):
    """ View generates javascript response that is used to load widget js files 
    should be public """
    model = Shop
    template_name = 'widget/for_shop.js'

    def get_context_data(self, **kwargs):
        context = super(WidgetsForShopView, self).get_context_data(**kwargs)

        static_url = self.request.build_absolute_uri(settings.STATIC_URL)

        default_scripts = [
            '%semberjs/js/libs/ember-0.9.8.1.min.js'%(static_url),
            '%semberjs/js/libs/ember-data-latest.js'%(static_url),
            '%semberjs/js/libs/tastypie_adapter.js'%(static_url),
            #'%semberjs/js/libs/ember-facebook.js'%(static_url),
            #'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.13/jquery-ui.min.js',
        ]

        widget_list = Widget.objects.filter(shop=self.object, widget_type=Widget.WIDGET_TYPE.text_javascript)
        context['widget_list_init_names'] = [ w.slug.replace('-','_') for w in widget_list]

        context['scripts'] = default_scripts #+ [ '%s'%(self.request.build_absolute_uri(reverse('widget:script', kwargs={'shop_slug': self.object.slug, 'slug': widget.slug})),) for widget in widget_list ]

        context['scripts_script'] = []
        # for script in default_scripts:
        #     path_to_script = finders.find(script.replace(static_url,''))
        #     text = open(os.path.join(settings.STATIC_ROOT, path_to_script)).read()
        #     context['scripts_script'].append(text)

        # must be the last in this view as it needs a full context
        c = Context(context)
        templates = []
        combined_widgets = []
        for widget in widget_list:
            widget_shop_join = get_object_or_404(WidgetShop, widget=widget, shop=self.object)
            c['config'] = widget_shop_join.data

            template = '%s%s.js' %('widget/', widget.slug,)
            combined_widgets.append(loader.get_template(template).render(c))

            for template in widget.data['templates']:
                templates.append(loader.get_template(template).render(c))

        context['templates'] = templates
        core_combined_widget = ''.join(combined_widgets)
        context['combined_widgets'] = core_combined_widget

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

