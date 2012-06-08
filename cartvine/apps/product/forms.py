from django import forms
from django.utils.translation import ugettext_lazy as _
from bootstrap import forms as bootstrap
from bootstrap import widgets as bootstrap_widgets
from django.template.defaultfilters import slugify

from cartvine.utils import get_namedtuple_choices

class ProductVariantForm(bootstrap.BootstrapForm):
    sku = forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'span2'}))
    grams = forms.CharField(label=_('Weight'), widget=forms.widgets.TextInput(attrs={'class':'span1'}))
    title = forms.CharField()
    inventory_policy = forms.CharField()
    created_at = forms.CharField(widget=forms.widgets.HiddenInput())
    updated_at = forms.CharField(widget=forms.widgets.HiddenInput())
    inventory_quantity = forms.IntegerField()
    provider_id = forms.IntegerField(widget=forms.widgets.HiddenInput())
    price = forms.FloatField(label=_('Selling price'), widget=bootstrap_widgets.AppendedText(attrs={'class':'span1', 'text': '&euro;'}))
    compare_at_price = forms.CharField(label=_('Compare at price'), widget=bootstrap_widgets.AppendedText(attrs={'class':'span1', 'text': '&euro;'}))
    inventory_management = forms.ChoiceField(label=_('Inventory'), choices=(("Don't track stock level", _("Don't track stock level")), ("Shopify tracks this variant's stock level", _("Shopify tracks this variant's stock level"))))
    fulfillment_service = forms.CharField()
    position = forms.CharField()
    option1 = forms.CharField()
    option2 = forms.CharField()
    option3 = forms.CharField()
    requires_shipping = forms.BooleanField(label=_('Require shipping'))
    taxable = forms.BooleanField(label=_('Charge taxes'))

    class Meta:
        layout = (
                    bootstrap.Fieldset("Product Variant", 
                                    "sku", "grams", "title", "inventory_policy", "created_at", 
                                    "requires_shipping", "updated_at", "inventory_quantity", 
                                    "provider_id", "price", "inventory_management", 
                                    "fulfillment_service", "taxable", "position", "option1", 
                                    "option2", "option3", "compare_at_price"),
                                    )

    def save(self, commit=True):
        pass
