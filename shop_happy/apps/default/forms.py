from django import forms
from django.utils.translation import ugettext_lazy as _


class ShopifyInstallForm(forms.Form):
    shop = forms.CharField(label=_('Shop URL'), required=True, help_text=_('Enter the URL to your shop, or just its subdomain "your-shop-name".myshopify.com'))
