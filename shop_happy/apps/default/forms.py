from django import forms

class ShopifyInstallForm(forms.Form):
    shop = forms.CharField(required=True)
