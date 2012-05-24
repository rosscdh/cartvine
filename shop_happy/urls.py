from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from shop_happy.apps.api.public import v1_public_api as v1_api

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # Api
    url(r'^api/', include(v1_api.urls)),
    # Core Application
    url(r'^webhook/', include('shop_happy.apps.webhook.urls', namespace='webhook')),
    url(r'^mail/', include('shop_happy.apps.mail.urls', namespace='mail')),
    url(r'^customer/', include('shop_happy.apps.customer.urls', namespace='customer')),
    url(r'^reviews/', include('shop_happy.apps.product_review.urls', namespace='review')),
    url(r'^products/', include('shop_happy.apps.product.urls', namespace='product')),
    url(r'^app/', include('shop_happy.apps.app_settings.urls', namespace='my_app')),
    url(r'^', include('shop_happy.apps.default.urls', namespace='default')),
)

urlpatterns += staticfiles_urlpatterns()
