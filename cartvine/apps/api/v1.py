from django.conf.urls.defaults import url
from django.utils import simplejson as json
import ast

from tastypie.resources import ModelResource
from tastypie.validation import FormValidation
from tastypie.api import Api
from tastypie.serializers import Serializer
from tastypie import fields, utils
from tastypie.resources import Resource
from tastypie.cache import SimpleCache

from authentication import OAuthAuthentication
from authorization import OAuthAuthorization

from cartvine.apps.product.models import Product, ProductVariant
from cartvine.apps.shop.models import Shop
from cartvine.apps.customer.models import Customer
from cartvine.apps.widget.models import Widget, WidgetShop

from facebook_user.apps.person.models import Person


v1_public_api = Api(api_name='v1')

available_formats = ['json','yaml']


class CartvineBaseModelResource(ModelResource):
    """
    Base Resource that all other api resources extend
    used to apply our filters and specific rulesets
    """
    class Meta:
        serializer = Serializer(formats=available_formats)
        authentication = OAuthAuthentication()
        authorization = OAuthAuthorization()

    def get_object_list(self, request):
        """ Test for a set of catch field names 
        These keys relate to references to models that need to be filtered by
        the current users company/customer id """
        try:
            self._meta.queryset = self._meta.queryset.model.objects.apply_api_user_filter(request.user)
        except AttributeError:
            pass

        return super(CartvineBaseModelResource, self).get_object_list(request)


class ShopResource(CartvineBaseModelResource):
    class Meta:
        queryset = Shop.objects.all()
        resource_name = 'shop'
        serializer = Serializer(formats=available_formats)


class ProductResource(CartvineBaseModelResource):
    shop = fields.ForeignKey(ShopResource, 'shop')
    class Meta:
        queryset = Product.objects.all()
        resource_name = 'product'
        serializer = Serializer(formats=available_formats)
        filtering = {
            'shop': ('exact',),
            'slug': ['exact'],
        }

    def dehydrate(self, bundle):
        data = ast.literal_eval(bundle.data['data'])
        bundle.data['slug'] = data['handle'] # Override the local slug value as it is NOT the remote one necessarily, handle is always updated form teh shop
        bundle.data['vendor_id'] = data['id']
        bundle.data['featured_image'] = data['featured_image']
        bundle.data['tags'] = data['tags']
        bundle.data['product_type'] = data['product_type']
        bundle.data['vendor'] = data['vendor']
        bundle.data['properties_basic'] = data['options'] if 'options' in data else None
        bundle.data['properties_plus'] = data['properties_plus'] if 'properties_plus' in data else None

        del(bundle.data['data'])
        return bundle


class ProductPropertiesResource(ProductResource):
    class Meta:
        queryset = Product.objects.all()
        resource_name = 'product_properties'
        serializer = Serializer(formats=available_formats)
        filtering = {
            'shop': ('exact',),
            'slug': ['exact'],
        }
    def dehydrate(Self, bundle):
        data = ast.literal_eval(bundle.data['data'])
        options_list = []
        if 'options' in data:
            for v in data['options']:
                options_list.append(v['name'])

        if 'properties_plus' in data:
            for k,v in data['properties_plus'].iteritems():
                options_list.append(v)

        c = 1
        for i in options_list:
            bundle.data['option%s'%(c,)] = i
            c = c+1
        bundle.data['num_items'] = len(options_list)
        del(bundle.data['data'])
        return bundle


class ProductVariantResource(CartvineBaseModelResource):
    product = fields.ForeignKey(ProductResource, 'product')
    class Meta:
        queryset = ProductVariant.objects.all()
        resource_name = 'variant'
        serializer = Serializer(formats=available_formats)
        filtering = {
            'product': ['exact'],
            'provider_id': ['exact'],
            'slug': ['exact'],
            'name': ['exact']
        }

    def dehydrate(self, bundle):
        data = ast.literal_eval(bundle.data['data'])

        bundle.data['provider_id'] = data['id'] if 'id' in data else None
        bundle.data['title'] = data['title'] if 'title' in data else None
        bundle.data['sku'] = data['sku']
        bundle.data['grams'] = data['grams']
        bundle.data['inventory_policy'] = data['inventory_policy']
        bundle.data['created_at'] = data['created_at'] if 'created_at' in data else None
        bundle.data['updated_at'] = data['updated_at'] if 'updated_at' in data else None
        bundle.data['requires_shipping'] = data['requires_shipping']
        bundle.data['inventory_quantity'] = data['inventory_quantity']
        bundle.data['price'] = data['price']
        bundle.data['inventory_management'] = data['inventory_management'] if 'inventory_management' in data else None
        bundle.data['fulfillment_service'] = data['fulfillment_service'] if 'fulfillment_service' in data else None
        bundle.data['taxable'] = data['taxable']
        bundle.data['position'] = data['position'] if 'position' in data else None
        bundle.data['option1'] = data['option1']
        bundle.data['option2'] = data['option2']
        bundle.data['option3'] = data['option3']
        bundle.data['compare_at_price'] = data['option3']

        del(bundle.data['data'])
        return bundle

class CustomerResource(CartvineBaseModelResource):
    class Meta:
        queryset = Customer.objects.all()
        resource_name = 'customer'
        serializer = Serializer(formats=available_formats)


class PersonResource(CartvineBaseModelResource):
    class Meta:
        queryset = Person.objects.all()
        resource_name = 'person'
        serializer = Serializer(formats=available_formats)


class WidgetResource(CartvineBaseModelResource):
    class Meta:
        queryset = Widget.objects.all()
        resource_name = 'widget'
        serializer = Serializer(formats=available_formats)

class WidgetShopResource(CartvineBaseModelResource):
    class Meta:
        queryset = WidgetShop.objects.all()
        resource_name = 'widget_config'
        serializer = Serializer(formats=available_formats)


""" Register the api resources """
v1_public_api.register(ProductResource())
v1_public_api.register(ProductPropertiesResource())
v1_public_api.register(ProductVariantResource())
v1_public_api.register(ShopResource())
v1_public_api.register(CustomerResource())
v1_public_api.register(WidgetResource())
v1_public_api.register(WidgetShopResource())

""" Facebook Users """
v1_public_api.register(PersonResource())
