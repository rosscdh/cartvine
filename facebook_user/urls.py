from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # Facebook User Application
    url(r'^', include('facebook_user.apps.default.urls', namespace='default')),
)
