from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.template import loader, Context

from cartvine.apps.shop.models import Shop

from models import Widget, WidgetShop
from forms import CustomerWidgetEditForm


class MyWidgetView(ListView):
    model = Widget

    def get_queryset(self):
        shop = Shop.objects.filter(users__in=[self.request.user])
        return Widget.objects.filter(shop=shop)


class MyWidgetEditView(FormView):
    form_class = CustomerWidgetEditForm
    template_name = 'widget/widget_edit.html'

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
    model = Shop
    template_name = 'widget/for_shop.html'

    def get_context_data(self, **kwargs):
        context = super(WidgetsForShopView, self).get_context_data(**kwargs)

        static_url = self.request.build_absolute_uri(settings.STATIC_URL)

        default_scripts = [
            '%semberjs/js/libs/ember-0.9.8.1.min.js'%(static_url),
            #'%semberjs/js/libs/ember-data-latest.min.js'%(static_url),
            #'%semberjs/js/libs/tastypie_adapter.js'%(static_url),
            #'%semberjs/js/libs/ember-facebook.js'%(static_url),
        ]

        widget_list = Widget.objects.filter(shop=self.object)

        context['scripts'] = default_scripts + [ '%s'%(self.request.build_absolute_uri(reverse('widget:script', kwargs={'shop_slug': self.object.slug, 'slug': widget.slug})),) for widget in widget_list ]

        # must be the last in this view as it needs a full context
        c = Context(context)
        templates = []
        for widget in widget_list:
            for template in widget.data['templates']:
                templates.append(loader.get_template(template).render(c))

        context['templates'] = templates
        return context


class SpecificWidgetForShopView(DetailView):
    model = Widget
    template_name = 'widget/widget.js'

    def get_context_data(self, **kwargs):
        context = super(SpecificWidgetForShopView, self).get_context_data(**kwargs)

        widget_shop_join = get_object_or_404(WidgetShop, widget=self.object)
        context['config'] = widget_shop_join.data
        context['shop'] = get_object_or_404(Shop, slug=self.kwargs['shop_slug'])
        
        script_name = '%s%s.js' %('widget/', self.object.slug,)
        self.template_name = script_name

        return context
