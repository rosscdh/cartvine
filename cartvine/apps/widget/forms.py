from django import forms
from django.utils.translation import ugettext_lazy as _
from bootstrap import forms as bootstrap
from bootstrap import widgets as bootstrap_widgets

from models import Widget


class BaseWidgetEditForm(bootstrap.BootstrapForm):
    target_id = forms.CharField(_('Target ID'), help_text=_('The div#id_name or the html element name that you want to inject your widget into'), required=True, initial='body', widget=bootstrap_widgets.PrependedText)

    class Meta:
        layout = (bootstrap.Fieldset("Configure your widget", "target_id"),)

class FacebookAuthWidgetForm(BaseWidgetEditForm):
    pass