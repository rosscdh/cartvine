from django.conf import settings
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse

from views import WidgetLoaderView, WidgetsForShopView, SpecificWidgetForShopView


urlpatterns = patterns('',
    url(r'^cartvine-loader\.js$', WidgetLoaderView.as_view(), name='widget_loader'),
    url(r'^(?P<shop_slug>.+)/(?P<slug>.+)/$', SpecificWidgetForShopView.as_view(), name='script'),
    url(r'^(?P<slug>.+)/$', WidgetsForShopView.as_view(), name='for_shop'),
)
