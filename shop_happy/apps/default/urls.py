from django.conf.urls import patterns, include, url

from views import DefaultView


urlpatterns = patterns('',
    url(r'^$', DefaultView.as_view(), name='index'),
)
