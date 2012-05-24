from django.conf.urls.defaults import url

from tastypie.resources import ModelResource
from tastypie.validation import FormValidation
from tastypie.api import Api
from tastypie.serializers import Serializer
from tastypie import fields, utils
from tastypie.resources import Resource
from tastypie.cache import SimpleCache

from authentication import AdcloudOAuthAuthentication
from authorization import AdcloudOAuthAuthorization

from shop_happy.apps.product.models import Product



v1_public_api = Api(api_name='v1')

available_formats = ['json','yaml']


class ShopHappyBaseModelResource(ModelResource):
    """
    Base Resource that all other api resources extend
    used to apply our filters and specific rulesets
    """
    class Meta:
        serializer = Serializer(formats=available_formats)
        authentication = AdcloudOAuthAuthentication()
        authorization = AdcloudOAuthAuthorization()

    def get_object_list(self, request):
        """ Test for a set of catch field names 
        These keys relate to references to models that need to be filtered by
        the current users company/customer id """
        try:
            self._meta.queryset = self._meta.queryset.model.objects.apply_api_user_filter(request.user)
        except AttributeError:
            pass

        return super(AdcloudBaseModelResource, self).get_object_list(request)


class ProductResource(ShopHappyBaseModelResource):
    class Meta:
        queryset = Product.objects.all()
        resource_name = 'products'
        serializer = Serializer(formats=available_formats)


""" Register the api resources """
v1_public_api.register(ProductResource())