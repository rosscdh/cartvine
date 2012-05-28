from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView, RedirectView

from forms import AppSettingsForm

import shopify


class SettingsView(TemplateView):
    template_name = 'app_settings/settings.html'

    def get(self, request, *args, **kwargs):
        form = AppSettingsForm()

        return self.render_to_response({
            'form': form,
        })

class DesignView(TemplateView):
    template_name = 'app_settings/design.html'

