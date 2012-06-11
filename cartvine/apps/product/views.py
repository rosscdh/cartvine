from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView

import shopify
from annoying.decorators import ajax_request

from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery

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


@ajax_request
def ProductSearchView(request):
    #object_list = Product.objects.by_shopify_owner(request.user).all()
    query = request.GET.get('q', None)
    if query is not None:
    	object_list = SearchQuerySet().using('default').filter(content__contains=query)
    else:
    	object_list = SearchQuerySet().using('default').all()

    ajax_object_list = [{'name':p.name, 'shop':p.shop, 'provider_id':p.provider_id, 'slug':p.slug, 'tags':p.tags, 'image': p.featured_image_src} for p in object_list]

    return {
    'products': ajax_object_list
    }
