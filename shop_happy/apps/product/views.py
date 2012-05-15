from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse

from django.views.generic import DetailView, ListView

import shopify

from models import Product


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        product_list = shopify.Product.find(limit=3)
        return {
            'object_list': product_list
        }
