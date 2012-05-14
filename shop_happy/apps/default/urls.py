from django.conf.urls import patterns, include, url

from views import DefaultView, FinalizeInstallationView


urlpatterns = patterns('',
    
    url(r'^finalize/$', FinalizeInstallationView.as_view(), name='finalize'),
    url(r'^', DefaultView.as_view(), name='index'),
)
