from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from cartvine.utils import login_required
from django.views.decorators.csrf import csrf_exempt

from cartvine.decorators import shop_login_required

from views import PersonValidationView


urlpatterns = patterns('',
    # Account Validation
    url(r'^validate/(?P<application_type>\w+)/$', csrf_exempt(PersonValidationView.as_view()), name='validate'),
)
