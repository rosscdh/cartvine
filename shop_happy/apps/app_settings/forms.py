from django import forms
from django.utils.translation import ugettext_lazy as _


class AppSettingsForm(forms.Form):
    SEND_EMAIL = (
        (0, _('Same Day')),
        (1, _('Next Day')),
        (2, _('Same Week')),
        (3, _('Next Week')),
        (4, _('2 Weeks')),
    )
    send_email = forms.ChoiceField(choices=SEND_EMAIL, required=True, help_text=_('When should we send the product review invitation email'))
