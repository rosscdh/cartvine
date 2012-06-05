import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, DetailView, ListView, FormView, RedirectView
from django.template import loader, Context
from django.contrib.admin.views.main import ChangeList

from cartvine.apps.widget.forms import ShopPropsWidgetForm


class ShopExtendView(FormView):
    template_name = 'widget/shop_prop/widget_edit.html'

    def get_form_class(self):
        return ShopPropsWidgetForm

    def get_success_url(self):
        return reverse('widget:custom_edit', kwargs={'slug': self.kwargs['slug']})

    def get_initial(self):
        return {}

    def get_context_data(self, **kwargs):
        context = super(ShopExtendView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        if form.is_valid():
            pass
        return super(ShopExtendView, self).post(request, *args, **kwargs)
    