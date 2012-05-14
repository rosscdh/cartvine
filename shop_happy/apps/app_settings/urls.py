from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse

from shop_happy.decorators import shop_login_required

from views import SettingsView, DesignView


urlpatterns = patterns('',
    url(r'^settings/$', shop_login_required(SettingsView.as_view()), name='settings'),
    url(r'^design/$', shop_login_required(DesignView.as_view()), name='design'),

)
