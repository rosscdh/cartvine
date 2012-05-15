from django.conf import settings
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse

from shop_happy.decorators import shop_login_required

from views import SettingsView, DesignView


urlpatterns = patterns('',
    url(r'^settings/$', SettingsView.as_view(), name='settings'),
    url(r'^design/$', DesignView.as_view(), name='design'),
)
