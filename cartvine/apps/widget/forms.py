from django import forms
from django.utils.translation import ugettext_lazy as _
from bootstrap import forms as bootstrap
from bootstrap import widgets as bootstrap_widgets
from django.template.defaultfilters import slugify

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
    name = forms.CharField(_('Property Name'),help_text=_('eg. Color, Size, Type...'),required=True)
    value = forms.CharField(_('Property Value'),help_text=_('Green;Red;Blue ... use ; to seperate. or leave blank'),required=True)

    class Meta:
        layout = (bootstrap.Fieldset("Custom Properties", "name", "value"),)

    def save(self, widget_shop_config, commit=True):
        if 'name' in self.cleaned_data and 'value' in self.cleaned_data:
            if 'extended_props' not in widget_shop_config.data:
                widget_shop_config.data['extended_props'] = dict({})
                widget_shop_config.data['extended_props']['product'] = []

            #safe_name = slugify(self.cleaned_data['name'])
            widget_shop_config.data['extended_props']['product'].append({'name': self.cleaned_data['name'], 'value': self.cleaned_data['value']})

            return widget_shop_config.save()
        else:
            return False

