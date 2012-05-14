from django.conf.urls import patterns, include, url

from views import SettingsView, DesignView

urlpatterns = patterns('',
    
    url(r'^settings/$', SettingsView.as_view(), name='settings'),
    url(r'^design/$', DesignView.as_view(), name='design'),
)
