import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, DetailView, ListView, FormView, RedirectView
from django.template import loader, Context
from django.contrib.admin.views.main import ChangeList
from django.forms.formsets import formset_factory

from cartvine.apps.widget.forms import ShopPropsWidgetForm
from cartvine.apps.widget.models import Widget, WidgetShop
from cartvine.apps.shop.models import Shop


class ShopExtendView(FormView):
    template_name = 'widget/shop_prop/widget_edit.html'

    def get_form_class(self):
        return formset_factory(ShopPropsWidgetForm, extra=3)

    def get_success_url(self):
        return reverse('widget:custom_edit', kwargs={'slug': self.kwargs['slug']})

    def get_initial(self):
        shop = Shop.objects.filter(users__in=[self.request.user])
        self.widget_config = get_object_or_404(WidgetShop.objects.filter(shop=shop), widget__slug=self.kwargs['slug'])
        return self.widget_config.data['extended_props']['product'] if 'extended_props' in self.widget_config.data and 'product' in self.widget_config.data['extended_props'] else {}

    def get_context_data(self, **kwargs):
        context = super(ShopExtendView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())

        if form.is_valid():

            for f in form:
                f.save(self.widget_config)

        return super(ShopExtendView, self).post(request, *args, **kwargs)
    
