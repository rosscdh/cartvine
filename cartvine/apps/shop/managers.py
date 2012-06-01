from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured

import shopify
from urlparse import urlparse




class ShopManager(models.Manager):
    """ Manager for Shop objects 
    Provides accessor methods that wrap around the shopify api
    """
    def get_or_create_shop(self, shopify_session):
        """ Get or Create the Shop from the session if it does not exist
        also updates data from shopify api """
        # session is not present yet so create it
        # @TODO change this to use the Shop.activate_shopify_session() method
        shopify.ShopifyResource.activate_session(shopify_session)

        current_shop = shopify.Shop.current()

        shop, is_new = self.get_or_create(provider_id=current_shop.id)
        shop.data = current_shop.__dict__['attributes']
        shop.name = shop.data['name']

        slug = shop.data['myshopify_domain'].split('.')[0]
        shop.slug = slug

        shop.shopify_access_token = shopify_session.token
        shop.url = 'http://%s' % (shop.data['myshopify_domain'],)
        shop.save()

        return shop

    def get_or_create_owner(self, shop):
        """ Get/Create the owner for this Shop 
        depending if it exists or not """
        name = shop.data['shop_owner']
        # @TODO add try except here for if the name has no spaces
        first_name = name.split(' ')[0]
        last_name = ' '.join(name.split(' ')[1:])
        # @TODO could be more than 1 john smith at shop id 129989
        unique_id = '%d-%s' %(shop.data['id'], last_name,)
        username = slugify(unique_id)
        email = shop.data['email']
        user, is_new = User.objects.get_or_create(username=username, email=email, first_name=first_name, last_name=last_name)
        # if is new or is not new but for some reason was not assocaited with this shop (could be an existing customer that has no association with this shop, potential bug here if we have multiple 1-john-smiths)
        if is_new or not shop.users.filter(pk=user.pk).exists():
            shop.users.add(user)
        return user

