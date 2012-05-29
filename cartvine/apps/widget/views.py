from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView

from cartvine.apps.shop.models import Shop


class WidgetsForShopView(DetailView):
    model = Shop
    template_name = 'widget/for_shop.html'

    def get_context_data(self, **kwargs):
        context = super(WidgetsForShopView, self).get_context_data(**kwargs)

        script_list = [ '%s%s'%(self.request.build_absolute_uri(settings.STATIC_URL), s) for s in ['widget/widget-auth-facebook.js'] ]

        context['shop'] = self.object
        context['scripts'] = script_list

        return context
