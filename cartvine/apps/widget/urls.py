from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from views import AvailableWidgetView, WidgetInfoView, MyWidgetView, MyWidgetEditView
from views import WidgetLoaderView, WidgetsForShopView, SpecificWidgetForShopView


urlpatterns = patterns('',
    url(r'^my/(?P<slug>.+)/$', login_required(MyWidgetEditView.as_view()), name='edit'),
    url(r'^my/$', login_required(MyWidgetView.as_view()), name='my'),
    url(r'^cartvine-loader\.js$', WidgetLoaderView.as_view(), name='widget_loader'),

    url(r'^(?P<shop_slug>.+)/(?P<slug>.+)/$', SpecificWidgetForShopView.as_view(), name='script'),
    url(r'^(?P<slug>.+)/$', WidgetsForShopView.as_view(), name='for_shop'),

    url(r'^(?P<slug>.+)/info/$', login_required(WidgetInfoView.as_view()), name='info'),
    url(r'^$', login_required(AvailableWidgetView.as_view()), name='default'),
)
