from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import View

from shop_happy.apps.customer.models import Customer

import logging
logger = logging.getLogger('facebook_user')


class CustomerView(View):
    queryset = Customer.objects.all()
    def post(self, request, *args, **kwargs):
        print 'fdafdsa'
        return HttpResponse()
