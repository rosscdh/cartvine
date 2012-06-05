import os
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, DetailView, ListView, FormView, RedirectView
from django.template import loader, Context
from django.contrib.admin.views.main import ChangeList
from django.forms.formsets import formset_factory

from cartvine.apps.widget.forms import ShopPropsWidgetForm
from cartvine.apps.widget.models import Widget, WidgetShop
from cartvine.apps.widget.views.base import MyWidgetEditView

from cartvine.apps.shop.models import Shop
from cartvine.apps.product.models import Product


class ShopExtendConfigView(FormView):
    template_name = 'widget/shop_prop/widget_config.html'

    def get_form_class(self):
        return formset_factory(ShopPropsWidgetForm, extra=1, can_delete=True)

    def get_success_url(self):
        return reverse('widget:custom_config', kwargs={'slug': self.kwargs['slug']})

    def get_initial(self):
        shop = Shop.objects.filter(users__in=[self.request.user])
        self.widget_config = get_object_or_404(WidgetShop.objects.filter(shop=shop), widget__slug=self.kwargs['slug'])
        if 'extended_props' in self.widget_config.data and 'product' in self.widget_config.data['extended_props']:
            return self.widget_config.data['extended_props']['product']
        else:
            return {}

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())

        if form.is_valid():
            messages.success(request, _('You have Successfully saved your config settings'))
            for f in form:
                f.save(self.widget_config)

        return super(ShopExtendConfigView, self).post(request, *args, **kwargs)


class ShopExtendApplyView(DetailView):
    model = Product
    template_name = 'widget/shop_prop/product_edit.html'

    def get_object(self):
        shop = Shop.objects.filter(users__in=[self.request.user])
        self.widget_config = get_object_or_404(WidgetShop.objects.filter(shop=shop), widget__slug=self.kwargs['slug'])
        return self.model.objects.get(provider_id=self.request.GET.get('id'))

    def get_context_data(self, **kwargs):
        context = super(ShopExtendApplyView, self).get_context_data(**kwargs)
        context['widget_slug'] = self.kwargs['slug']
        context['widget_config'] = self.widget_config
        return context