from django import forms
from django.utils.translation import ugettext_lazy as _
from bootstrap import forms as bootstrap
from bootstrap import widgets as bootstrap_widgets
from django.template.defaultfilters import slugify

from cartvine.utils import get_namedtuple_choices
from models import Product, ProductVariant


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


class ProductPropertiesForm(forms.ModelForm):
    class Meta:
        model = Product

    def clean(self):
        cleaned_data = super(ProductPropertiesForm, self).clean()
        return cleaned_data


class ProductVariantForm(forms.Form):
    sku = forms.CharField(initial='',required=True)
    price = forms.FloatField(initial=1.00,required=True)
    provider_id = forms.IntegerField(required=False)
    compare_at_price = forms.CharField(initial=0,required=False)
    grams = forms.CharField(initial=0,required=False)
    inventory_policy = forms.CharField(initial='',required=False)
    requires_shipping = forms.BooleanField(initial=True,required=False)
    taxable = forms.BooleanField(initial=True,required=False)
    inventory_quantity = forms.IntegerField(initial=0,required=False)

    def clean(self):
        cleaned_data = super(ProductVariantForm, self).clean()
        if len(self.errors) > 0:
            return cleaned_data

        slug_parts = []

        # Set default values; all items in this form are "required"
        for k,c in self.fields.items():
            if k not in cleaned_data or cleaned_data[k] in [None,'None','null','']:
                cleaned_data[k] = self.fields[k].initial

        for c in range(1,4):
            # Deal with the current options1-3
            key = 'option%d'%(c,)
            cleaned_data[key] = self.data.get(key)
            slug_parts.append(str(cleaned_data[key]))


        if len(self.data.getlist('extra_props')) > 0:
            #slug_parts.append(cleaned_data[key])
            pass

        if slug_parts is not None and len(slug_parts) > 0:
            variant_slug = slugify(' '.join(slug_parts))
        else:
            random.randint(1, 100) #@TODO uuuglee fix this case
            variant_slug = '%s-%s' % (random,self.initial['product'].slug,)

        if self.initial['variant'] is None:
            variant, is_new = ProductVariant.objects.get_or_create(product=self.initial['product'], slug=variant_slug)
            variant.data = {}
            variant.save()
            self.initial['variant'] = variant

        if self.initial['variant'].slug in [None,'']:
            self.initial['variant'].slug = variant_slug

        cleaned_data['provider_id'] = self.initial['variant'].provider_id if hasattr(self.initial['variant'], 'provider_id') else None

        return cleaned_data

    def save(self):
        for key, value in self.cleaned_data.items():
            self.initial['variant'].data[key] = value

        self.initial['variant'].sku = self.initial['variant'].data['sku']
        self.initial['variant'].inventory_quantity = self.initial['variant'].data['inventory_quantity']

        self.initial['variant'].save()
        return self.initial['variant']

