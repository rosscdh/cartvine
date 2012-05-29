from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from cartvine.apps.api.v1 import v1_public_api

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # Api
    url(r'^api/', include(v1_public_api.urls)),
    # Widget JS Loader
    url(r'^widget/', include('cartvine.apps.widget.urls', namespace='widget')),
    # Core Application
    url(r'^webhook/', include('cartvine.apps.webhook.urls', namespace='webhook')),
    url(r'^mail/', include('cartvine.apps.mail.urls', namespace='mail')),
    url(r'^customer/', include('cartvine.apps.customer.urls', namespace='customer')),
    url(r'^reviews/', include('cartvine.apps.product_review.urls', namespace='review')),
    url(r'^products/', include('cartvine.apps.product.urls', namespace='product')),
    url(r'^app/', include('cartvine.apps.app_settings.urls', namespace='my_app')),
    url(r'^', include('cartvine.apps.default.urls', namespace='default')),
)

urlpatterns += staticfiles_urlpatterns()
