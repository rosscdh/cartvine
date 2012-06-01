from django import forms
from django.utils.translation import ugettext_lazy as _
from bootstrap import forms as bootstrap
from bootstrap import widgets as bootstrap_widgets


class ShopifyInstallForm(bootstrap.BootstrapForm):
    shop = forms.CharField(_('Shop'), required=True, help_text=_('Enter the URL to your shop, or just its subdomain "your-shop-name".myshopify.com'), widget=bootstrap_widgets.AppendedText(attrs={'text': '.myshopify.com'}))

    class Meta:
        layout = (bootstrap.Fieldset("Configure your widget", "target_id"),)