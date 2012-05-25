from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from shop_happy.decorators import shop_login_required

from views import CustomerView


urlpatterns = patterns('',
    # Account Validation
    url(r'^validate/$', csrf_exempt(CustomerView.as_view()), name='validate'),
)
