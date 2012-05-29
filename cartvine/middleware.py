"""
@NOTE this whole middleware class may not even be required;
as we initialize the shopify session oly when requesting 
items from their api
"""
from django import http
from django.conf import settings
from django.utils.text import compress_string
from django.utils.cache import patch_vary_headers
from django.core.urlresolvers import reverse

import re

import shopify

XS_SHARING_ALLOWED_ORIGINS = getattr(settings, 'XS_SHARING_ALLOWED_ORIGINS', '*')
XS_SHARING_ALLOWED_METHODS = getattr(settings, 'XS_SHARING_ALLOWED_METHODS', ['POST','GET','OPTIONS', 'PUT', 'DELETE'])


class ConfigurationError(StandardError):
    pass


class LoginProtection(object):
    def __init__(self):
        if not settings.SHOPIFY_API_KEY or not settings.SHOPIFY_API_SECRET:
            raise ConfigurationError("SHOPIFY_API_KEY and SHOPIFY_API_SECRET must be set in settings")
        shopify.Session.setup(api_key=settings.SHOPIFY_API_KEY,secret=settings.SHOPIFY_API_SECRET)

    def process_request(self, request):
        if hasattr(request, 'session') and 'shopify' in request.session:
			# @NOTE taken out due to the python api making a request to the shopify api every single request surely this is not right raise with shopify
            #shopify.ShopifyResource.activate_session(request.session['shopify'])
            pass
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    def process_response(self, request, response):
        shopify.ShopifyResource.site = None
        return response


class XsSharing(object):
    """
        This middleware allows cross-domain XHR using the html5 postMessage API.
         

        Access-Control-Allow-Origin: http://foo.example
        Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
    """
    def process_request(self, request):

        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
            response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS ) 
            
            return response

        return None

    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return response

        response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
        response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )

        return response
