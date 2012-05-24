from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from shop_happy.decorators import shop_login_required

from views import DefaultView,LoginView,LogoutView


urlpatterns = patterns('',
    # Local App Urls
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', login_required(LogoutView.as_view()), name='logout'),
    # Facebook Specific Urls
    url(r'^facebook_debug/', direct_to_template, {'template':'facebook_debug.html'}, name='fb-debug'),
    url('^channel\.html', direct_to_template, {'template':'channel.html'}, name='facebook_channel_receiver'),
    url(r'^$', DefaultView.as_view(), name='index'),
)