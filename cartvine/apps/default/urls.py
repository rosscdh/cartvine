from django.conf.urls import patterns, include, url

from django.contrib.auth.decorators import login_required
from cartvine.decorators import shop_login_required

from views import DefaultView, LogoutView, FinalizeInstallationView


urlpatterns = patterns('',
    url(r'^login/$', DefaultView.as_view(), name='login'),
    url(r'^logout/$', login_required(LogoutView.as_view()), name='logout'),
    url(r'^finalize/$', FinalizeInstallationView.as_view(), name='finalize'),
    url(r'^$', DefaultView.as_view(), name='index'),
)
