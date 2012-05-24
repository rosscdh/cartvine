from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView, RedirectView


import logging
logger = logging.getLogger('facebook_user')


class DefaultView(TemplateView):
    template_name = 'default/default.html'

    def get(self, request, *args, **kwargs):

        return self.render_to_response({
        })

