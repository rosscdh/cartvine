from django.conf.urls.defaults import url

from tastypie.resources import ModelResource
from tastypie.validation import FormValidation
from tastypie.api import Api
from tastypie.serializers import Serializer
from tastypie import fields, utils
from tastypie.resources import Resource
from tastypie.cache import SimpleCache

from authentication import OAuthAuthentication
from authorization import OAuthAuthorization

from cartvine.apps.product.models import Product
from cartvine.apps.shop.models import Shop
from cartvine.apps.customer.models import Customer
from cartvine.apps.widget.models import Widget

from facebook_user.apps.person.models import Person


v1_public_api = Api(api_name='v1')

available_formats = ['json','yaml']


class ShopHappyBaseModelResource(ModelResource):
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

        return super(ShopHappyBaseModelResource, self).get_object_list(request)


class ProductResource(ShopHappyBaseModelResource):
    class Meta:
        queryset = Product.objects.all()
        resource_name = 'products'
        serializer = Serializer(formats=available_formats)


class ShopResource(ShopHappyBaseModelResource):
    class Meta:
        queryset = Shop.objects.all()
        resource_name = 'shops'
        serializer = Serializer(formats=available_formats)


class CustomerResource(ShopHappyBaseModelResource):
    class Meta:
        queryset = Customer.objects.all()
        resource_name = 'customers'
        serializer = Serializer(formats=available_formats)


class PersonResource(ShopHappyBaseModelResource):
    class Meta:
        queryset = Person.objects.all()
        resource_name = 'person'
        serializer = Serializer(formats=available_formats)


class WidgetResource(ShopHappyBaseModelResource):
    class Meta:
        queryset = Widget.objects.all()
        resource_name = 'widget'
        serializer = Serializer(formats=available_formats)


""" Register the api resources """
v1_public_api.register(ProductResource())
v1_public_api.register(ShopResource())
v1_public_api.register(CustomerResource())
v1_public_api.register(WidgetResource())

""" Facebook Users """
v1_public_api.register(PersonResource())
