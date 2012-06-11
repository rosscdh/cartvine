from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from cartvine.utils import login_required
from cartvine.decorators import shop_login_required

from views import ProductListView, ProductDetailView, ProductSearchView


urlpatterns = patterns('',
    url(r'^search/$', login_required(ProductSearchView), name='search'),

    url(r'^(?P<slug>.*)/$', login_required(ProductDetailView.as_view()), name='info'),
    url(r'^$', login_required(ProductListView.as_view()), name='index'),
)
