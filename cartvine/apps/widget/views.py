from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView

from cartvine.apps.shop.models import Shop

import os


class WidgetsForShopView(DetailView):
    model = Shop
    template_name = 'widget/for_shop.html'

    def get_context_data(self, **kwargs):
        context = super(WidgetsForShopView, self).get_context_data(**kwargs)

        script_list = [ '%s'%(self.request.build_absolute_uri(reverse('widget:script', kwargs={'slug': self.object.slug, 'script_name': s})),) for s in ['widget-auth-facebook.js'] ]

        context['shop'] = self.object
        context['scripts'] = script_list

        return context

class SpecificWidgetForShopView(DetailView):
    model = Shop
    template_name = 'widget/widget.js'

    def get_context_data(self, **kwargs):
        context = super(SpecificWidgetForShopView, self).get_context_data(**kwargs)

        script_name = '%s%s' %('widgets/', self.kwargs['script_name'],)
        text = open(os.path.join(settings.STATIC_ROOT, script_name), 'rb').read()

        context['script'] = text

        return context
