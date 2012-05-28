from django.conf import settings
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from cartvine.decorators import shop_login_required

from views import SettingsView, DesignView


urlpatterns = patterns('',
    url(r'^settings/$', login_required(SettingsView.as_view()), name='settings'),
    url(r'^design/$', login_required(DesignView.as_view()), name='design'),
)
