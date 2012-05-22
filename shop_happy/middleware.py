"""
@NOTE this whole middleware class may not even be required;
as we initialize the shopify session oly when requesting 
items from their api
"""
from django.conf import settings
from django.core.urlresolvers import reverse
import shopify


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


