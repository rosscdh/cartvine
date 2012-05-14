from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^review/', include('shop_happy.apps.product_review.urls', namespace='review_product')),
    url(r'^app/', include('shop_happy.apps.app_settings.urls', namespace='myapp')),
    url(r'^', include('shop_happy.apps.default.urls', namespace='default')),
)
