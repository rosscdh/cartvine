from django.conf import settings
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

from views import InviteReviewView, CreateInvite


urlpatterns = patterns('',
    url(r'^invite/review/create/$', csrf_exempt(CreateInvite), name='invite_review_create'),
)
