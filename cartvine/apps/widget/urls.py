from django.conf import settings
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse

from views import WidgetsForShopView


urlpatterns = patterns('',
    url(r'^(?P<slug>.*)/$', WidgetsForShopView.as_view(), name='for_shop'),
)
