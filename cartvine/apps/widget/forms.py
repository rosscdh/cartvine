from django import forms
from django.utils.translation import ugettext_lazy as _
from bootstrap import forms as bootstrap
from bootstrap import widgets as bootstrap_widgets

from models import Widget


class CustomerWidgetEditForm(bootstrap.BootstrapForm):
    target_id = forms.CharField(_('Target ID'), help_text=_('The div#id_name of the html element you want to inject the widget into'), required=True, widget=bootstrap_widgets.PrependedText)

    class Meta:
        layout = (bootstrap.Fieldset("Configure your widget", "target_id"),)
