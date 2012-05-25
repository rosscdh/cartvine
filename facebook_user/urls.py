from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from shop_happy.apps.api.v1 import v1_public_api

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # Api
    url(r'^api/', include(v1_public_api.urls)),
    # Person & Validation
    url(r'^person/', include('facebook_user.apps.person.urls', namespace='person')),
    # Facebook User Application
    url(r'^', include('facebook_user.apps.default.urls', namespace='default')),
)

urlpatterns += staticfiles_urlpatterns()
