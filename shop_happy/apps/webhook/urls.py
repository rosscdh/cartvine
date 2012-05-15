from django.conf import settings
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse

from views import InviteReviewView


urlpatterns = patterns('',
    url(r'^invite/review/create/$', InviteReviewView.as_view(), name='invite_review_create'),
)
