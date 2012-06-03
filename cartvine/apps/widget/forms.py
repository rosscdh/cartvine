from django import forms
from django.utils.translation import ugettext_lazy as _
from bootstrap import forms as bootstrap
from bootstrap import widgets as bootstrap_widgets

from cartvine.utils import get_namedtuple_choices

from models import Widget


class BaseJavascriptWidgetEditForm(bootstrap.BootstrapForm):
    target_id = forms.CharField(_('Target ID'), help_text=_('The div#id_name or the html element name that you want to inject your widget into'), required=True, initial='body', widget=bootstrap_widgets.PrependedText(attrs={'prepend_text': '#'}))

    class Meta:
        layout = (bootstrap.Fieldset("Configure your Widget", "target_id"),)


class FacebookAuthWidgetForm(BaseJavascriptWidgetEditForm):
    pass


class ProductsLikeWidgetForm(BaseJavascriptWidgetEditForm):
    pass


class ShopPropsWidgetForm(bootstrap.BootstrapForm):
    PROPERTY_TYPES = get_namedtuple_choices('PROPERTY_TYPES', (
        ('string', 'string_single_input', 'Single Choice'),
        ('string', 'string_multiple_input', 'Multiple Choice'),
        ('string', 'string_user_defined', 'User Defined'),
    ))
    property_name = forms.CharField(_('Property Name'),help_text=_('eg. Color, Size, Type...'),required=True)
    property_type = forms.ChoiceField(label=_('Property Type'), choices=PROPERTY_TYPES.get_choices(),required=True)
    property_value = forms.CharField(_('Property Value'),help_text=_('Green;Red;Blue ... use ; to seperate. or leave blank'),required=True)

    class Meta:
        layout = (bootstrap.Fieldset("Configure your Application", "property_name", "property_value", "property_type"),)
