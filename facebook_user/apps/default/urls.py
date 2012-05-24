from django.conf.urls import patterns, include, url

from django.contrib.auth.decorators import login_required
from shop_happy.decorators import shop_login_required

from views import DefaultView


urlpatterns = patterns('',
    url(r'^$', DefaultView.as_view(), name='index'),
)
