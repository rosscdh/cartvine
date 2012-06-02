from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page

from views import AvailableWidgetView, WidgetInfoView, MyWidgetView, MyWidgetEditView
from views import WidgetLoaderView, WidgetsForShopView, SpecificWidgetForShopView, BuyWidgetView


urlpatterns = patterns('',
    url(r'^cartvine-loader\.js$', WidgetLoaderView.as_view(), name='widget_loader'),
    #url(r'^script/(?P<slug>[-\w]+)/$', cache_page(60, WidgetsForShopView.as_view()), name='for_shop'),
    url(r'^script/(?P<slug>[-\w]+)/$', WidgetsForShopView.as_view(), name='for_shop'),
    url(r'^script/(?P<shop_slug>[-\w]+)/(?P<slug>[-\w]+)/$', SpecificWidgetForShopView.as_view(), name='script'),

    url(r'^my/(?P<slug>[-\w]+)/$', login_required(MyWidgetEditView.as_view()), name='edit'),
    url(r'^my/$', login_required(MyWidgetView.as_view()), name='my'),

    url(r'^(?P<slug>[-\w]+)/info/$', login_required(WidgetInfoView.as_view()), name='info'),
    url(r'^(?P<slug>[-\w]+)/buy/$', login_required(BuyWidgetView.as_view()), name='buy'),

    url(r'^$', login_required(AvailableWidgetView.as_view()), name='default'),
)
