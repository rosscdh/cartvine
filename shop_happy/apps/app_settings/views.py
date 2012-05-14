from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView, RedirectView

import shopify


class SettingsView(TemplateView):
    template_name = 'app_settings/settings.html'


class DesignView(TemplateView):
    template_name = 'app_settings/design.html'

