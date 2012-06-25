from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import DetailView, ListView, FormView
from django.utils import simplejson as json
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify

from forms import ProductPropertiesForm, BaseProductPropertiesForm, BasicProductPropertiesForm, PlusProductPropertiesForm, ProductVariantForm
from models import Product, ProductVariant

import shopify
from annoying.decorators import ajax_request

from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery


class ProductListView(ListView):
    model = Product
    def get_context_data(self, **kwargs):
        object_list = Product.objects.by_shopify_owner(self.request.user).all()

        return {
        'object_list': object_list
        }


class ProductDetailView(DetailView):
    queryset = None
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


class ProductPropertiesView(FormView):
    form_class = ProductPropertiesForm

    def get_initial(self):
        self.initial['product'] = self.object = Product.objects.get(slug=self.kwargs['slug'])

        return self.initial.copy()

    def get_response_json(self):
        return {
            'pk': self.object.pk if hasattr(self, 'object') else None,
            'status': '',
            'message': '',
            'object': None,
        }

    def post(self, request, *args, **kwargs):

        form = self.get_form(self.get_form_class())

        response = self.get_response_json()
        if not form.is_valid():
            response['status'] = 'error'
            response['message'] = str(form.errors)
        else:
            try:
                variant = form.save()
                response['pk'] = variant.pk
                response['object'] = variant.data
                response['object']['pk'] = variant.pk
                response['object']['basic_options'] = variant.basic_options()

                response['status'] = 'success'
                response['message'] = unicode(_('Success, We saved your variant!'))
            except:
                response['status'] = 'error'
                response['message'] = unicode(_('Strange an error occurred; but were not sure what.'))

        return HttpResponse(json.dumps(response), content_type='text/json')


class BaseProductPropertiesView(ProductPropertiesView):
    form_class = BaseProductPropertiesForm

    def post(self, request, *args, **kwargs):

        form = self.get_form(self.get_form_class())

        response = self.get_response_json()

        if not form.is_valid():
            response['status'] = 'error'
            response['message'] = str(form.errors)
        else:
            try:
                product = form.save()
                response['pk'] = product.pk
                response['object'] = product.data
                response['object']['pk'] = product.pk

                response['status'] = 'success'
                response['message'] = unicode(_('Success, Product Property Updated'))
            except:
                response['status'] = 'error'
                response['message'] = unicode(_('Strange an error occurred; but were not sure what.'))

        return HttpResponse(json.dumps(response), content_type='text/json')


class BasicProductPropertiesView(ProductPropertiesView):
    form_class = BasicProductPropertiesForm

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())

        response = self.get_response_json()
        if not form.is_valid():
            response['status'] = 'error'
            response['message'] = str(form.errors)
        else:
            # try:
            product = form.save()
            response['pk'] = product.pk
            response['object'] = product.data
            response['object']['pk'] = product.pk

            response['status'] = 'success'
            response['message'] = unicode(_('Success, Product Property Updated'))
            # except:
            #     response['status'] = 'error'
            #     response['message'] = unicode(_('Strange an error occurred; but were not sure what.'))

        return HttpResponse(json.dumps(response), content_type='text/json')


class PlusProductPropertiesView(ProductPropertiesView):
    form_class = PlusProductPropertiesForm

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())

        response = self.get_response_json()
        if not form.is_valid():
            response['status'] = 'error'
            response['message'] = str(form.errors)
        else:
            # try:
            product = form.save()
            response['pk'] = product.pk
            response['object'] = product.data
            response['object']['pk'] = product.pk

            response['status'] = 'success'
            response['message'] = unicode(_('Success, Product Property Updated'))
            # except:
            #     response['status'] = 'error'
            #     response['message'] = unicode(_('Strange an error occurred; but were not sure what.'))

        return HttpResponse(json.dumps(response), content_type='text/json')


class ProductVariantView(FormView):
    form_class = ProductVariantForm

    def get_response_json(self):
        return {
            'pk': self.variant.pk if hasattr(self, 'variant') else None,
            'status': '',
            'message': '',
            'object': None,
        }

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ProductVariantView, self).get_form_kwargs(**kwargs)

        kwargs['initial']['product'] = self.product = get_object_or_404(Product, slug=self.kwargs['slug'])

        if 'variant_pk' not in self.kwargs:
            # is_new
            kwargs['initial']['variant'] = None
        else:
            # editing
            kwargs['initial']['variant'] = self.variant = get_object_or_404(ProductVariant, pk=self.kwargs['variant_pk'])

        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())

        response = self.get_response_json()
        if not form.is_valid():
            response['status'] = 'error'
            response['message'] = str(form.errors)
        else:
            try:
                variant = form.save()
                response['pk'] = variant.pk
                response['object'] = variant.data
                response['object']['pk'] = variant.pk
                response['object']['basic_options'] = variant.basic_options()

                response['status'] = 'success'
                response['message'] = unicode(_('Success, Variant Updated'))
            except:
                response['status'] = 'error'
                response['message'] = unicode(_('Strange an error occurred; but were not sure what.'))


        return HttpResponse(json.dumps(response), content_type='text/json')
