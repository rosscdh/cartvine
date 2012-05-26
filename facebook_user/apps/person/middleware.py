"""
The people middleware is deisgned to capture the PRODIDER_INFO
of the shop that the user has come from. The remote ShopOwner
Installs our javascript widget, which in turn loads up our 
come shop with us js app, ahile testing for https and various 
other aspects.. it then encodes the SHOP_URL and tries to identify
the user based on the remote shops user identification standard
"""
from django.conf import settings
from django.core.urlresolvers import reverse


class LoginProtection(object):

    def process_request(self, request):
        if 'PROVIDER_INFO' in request.GET:
			request.session.set('PROVIDER_INFO')
        return None
