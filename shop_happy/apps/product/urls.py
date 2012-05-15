from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from shop_happy.decorators import shop_login_required

from views import ProductListView


urlpatterns = patterns('',
    url(r'^', shop_login_required(ProductListView.as_view()), name='index'),
)
