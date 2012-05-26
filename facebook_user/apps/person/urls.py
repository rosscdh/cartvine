from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from shop_happy.decorators import shop_login_required

from views import PersonView


urlpatterns = patterns('',
    # Account Validation
    url(r'^validate/(?P<application_type>\w+)/$', csrf_exempt(PersonView.as_view()), name='validate'),
)
