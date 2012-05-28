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
        object_list = Product.objects.by_shopify_owner(self.request.user).all()

        return {
        'object_list': object_list
        }


class ProductDetailView(DetailView):
    queryset = Product.objects.filter(pk=-1)
    def get_queryset(self):
		return Product.objects.by_shopify_owner(self.request.user).all()