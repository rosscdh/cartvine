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
    value = forms.CharField(_('Default Value'),help_text=_('Leave blank if there is no default value'),required=False)
    DELETE = forms.BooleanField(required=False)

    class Meta:
        layout = (bootstrap.Fieldset("Custom Prop", "name", "value", "DELETE"),)

    def uniquiefy(self, L):
        found = set()
        for item in L:
            if item['name'] not in found:
                yield item
                found.add(item['name'])

    def save(self, widget_shop_config, commit=True):
        if 'name' in self.cleaned_data and 'value' in self.cleaned_data:
            if 'extended_props' not in widget_shop_config.data:
                widget_shop_config.data['extended_props'] = {}
                widget_shop_config.data['extended_props']['product'] = []

            #safe_name = slugify(self.cleaned_data['name'])
            name = self.cleaned_data['name']
            value = self.cleaned_data['value']
            delete = self.cleaned_data['DELETE']

            if delete is not True:
                widget_shop_config.data['extended_props']['product'].append({'name': name, 'value': value})

            # uniquiefy
            if len(widget_shop_config.data['extended_props']['product']) > 0:
                widget_shop_config.data['extended_props']['product'] = list(self.uniquiefy(widget_shop_config.data['extended_props']['product']))

            return widget_shop_config.save()
        else:
            return False

class ShopPropsWidgetApplyForm(ShopPropsWidgetForm):
    def __init__(self, *args, **kwargs):
        super(ShopPropsWidgetApplyForm,self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.widgets.HiddenInput()
        self.fields.pop('DELETE')

    def save(self, product, commit=True):
        if 'widget' not in product.data:
            product.data['widget'] = {}
        if 'app-shop-prop' not in product.data['widget']:
            product.data['widget']['app-shop-prop'] = []

        name = self.cleaned_data['name']
        value = self.cleaned_data['value']

        found = False
        for i in product.data['widget']['app-shop-prop']:
            if i['name'] == name:
                i['value'] = value
                found = True
                break

        if found == False:
            product.data['widget']['app-shop-prop'].append({'name': name, 'value': value})
            product.data['widget']['app-shop-prop'] = list(self.uniquiefy(product.data['widget']['app-shop-prop']))

        return product.save()