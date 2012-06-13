from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from cartvine.utils import login_required
from cartvine.decorators import shop_login_required

from views import ProductListView, ProductDetailView, ProductSearchView, ProductPropertiesView, ProductVariantView


urlpatterns = patterns('',
    url(r'^search/$', login_required(ProductSearchView), name='search'),

    url(r'^(?P<slug>.*)/variant/(?P<variant_pk>\d+)/properties/$', login_required(ProductVariantView.as_view()), name='variant'),
    # url(r'^(?P<slug>.*)/properties/$', login_required(csrf_exempt(ProductPropertiesView.as_view())), name='property'),

    url(r'^(?P<slug>.*)/$', login_required(ProductDetailView.as_view()), name='info'),
    url(r'^$', login_required(ProductListView.as_view()), name='index'),
)
