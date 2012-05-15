from django.conf.urls import patterns, include, url

from views import DefaultView, FinalizeInstallationView


urlpatterns = patterns('',
    url(r'^login/$', FinalizeInstallationView.as_view(), name='login'),
    url(r'^logout/$', FinalizeInstallationView.as_view(), name='logout'),
    url(r'^finalize/$', FinalizeInstallationView.as_view(), name='finalize'),
    url(r'^', DefaultView.as_view(), name='index'),
)
