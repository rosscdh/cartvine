from django import forms
from django.utils.translation import ugettext_lazy as _


class PersonValidationPostForm(forms.Form):
    uid = forms.CharField(required=True)
    access_token = forms.CharField(max_length=255,required=True)
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
