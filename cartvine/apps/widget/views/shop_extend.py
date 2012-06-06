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

from cartvine.apps.widget.forms import ShopPropsWidgetForm, ShopPropsWidgetApplyForm
from cartvine.apps.product.forms import ProductVariantForm
from cartvine.apps.widget.models import Widget, WidgetShop
from cartvine.apps.widget.views.base import MyWidgetEditView

from cartvine.apps.shop.models import Shop
from cartvine.apps.product.models import Product

from cartvine.apps.widget.tasks import sync_product_metadata


class ShopExtendConfigView(FormView):
    template_name = 'widget/shop_prop/widget_config.html'

    def get_form_class(self):
        return formset_factory(ShopPropsWidgetForm, extra=1, can_delete=True)

    def get_success_url(self):
        return reverse('widget:custom_config', kwargs={'slug': self.kwargs['slug']})

    def get_initial(self):
        shop = Shop.objects.filter(users__in=[self.request.user])[0]
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


class ShopExtendApplyView(ShopExtendConfigView):
    model = Product
    template_name = 'widget/shop_prop/product_edit.html'

    def get_form_class(self):
        return formset_factory(ShopPropsWidgetApplyForm, extra=0, can_delete=False)

    def get_success_url(self):
        return reverse('widget:custom_apply_post', kwargs={'slug': self.kwargs['slug'], 'provider_pk': self.kwargs['provider_pk']})

    def get_initial(self):
        self.shop = Shop.objects.filter(users__in=[self.request.user])[0]
        self.widget_config = get_object_or_404(WidgetShop.objects.filter(shop=self.shop), widget__slug=self.kwargs['slug'])

        self.provider_pk = self.request.GET.get('id') if 'id' in self.request.GET else self.kwargs['provider_pk']
        self.kwargs['provider_pk'] = int(self.provider_pk)

        self.object = self.model.objects.get(provider_id=self.provider_pk)

        if 'extended_props' in self.widget_config.data and 'product' in self.widget_config.data['extended_props']:
            if 'widget' in self.object.data and 'app-shop-prop' in self.object.data['widget']:
                for key in self.widget_config.data['extended_props']['product']:
                    for i in self.object.data['widget']['app-shop-prop']:
                        if i['name'] == key['name']:
                            key['value'] = i['value']

            return self.widget_config.data['extended_props']['product']
        else:
            return {}

    def get_context_data(self, **kwargs):
        context = super(ShopExtendApplyView, self).get_context_data(**kwargs)        
        context['object'] = self.object
        context['variants'] = self.object.productvariant_set.all()
        variants = [v.data for v in context['variants']]
        variant_formset = formset_factory(ProductVariantForm, extra=0, can_delete=False)
        context['variant_form'] = variant_formset(initial=variants)
        context['widget_slug'] = self.kwargs['slug']
        context['provider_pk'] = self.kwargs['provider_pk']
        context['widget_config'] = self.widget_config

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        self.object = self.model.objects.get(provider_id=self.kwargs['provider_pk'])

        if form.is_valid():
            messages.success(request, _('You have Successfully saved your config settings'))
            for f in form:
                f.save(self.object)
            try:
                sync_product_metadata.delay(self.shop, self.object)
            except:
                sync_product_metadata(self.shop, self.object)

        return super(FormView, self).post(request, *args, **kwargs)

