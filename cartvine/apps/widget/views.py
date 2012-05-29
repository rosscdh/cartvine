from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView

from cartvine.apps.shop.models import Shop
from models import Widget


class WidgetsForShopView(DetailView):
    model = Shop
    template_name = 'widget/for_shop.html'

    def get_context_data(self, **kwargs):
        context = super(WidgetsForShopView, self).get_context_data(**kwargs)

        widget_list = Widget.objects.filter(shop=self.object)

        context['scripts'] = [ '%s'%(self.request.build_absolute_uri(reverse('widget:script', kwargs={'shop_slug': self.object.slug, 'slug': s.slug})),) for s in widget_list ]

        return context

class SpecificWidgetForShopView(DetailView):
    model = Widget
    template_name = 'widget/widget.js'

    def get_context_data(self, **kwargs):
        context = super(SpecificWidgetForShopView, self).get_context_data(**kwargs)

        context['shop'] = shop = get_object_or_404(Shop.objects.get(slug=self.kwargs['shop_slug']))

        script_name = '%s%s.js' %('widget/', self.object.slug,)
        self.template_name = script_name

        return context
