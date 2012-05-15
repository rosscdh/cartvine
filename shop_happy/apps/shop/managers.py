from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
import shopify

from django.contrib.auth.models import User


class ShopManager(models.Manager):
    """ Manager for Shop objects 
    Provides accessor methods that wrap around the shopify api
    """
    def get_or_create_shop(self, shopify_session):
        """ Get or Create the Shop from the session if it does not exist
        also updates data from shopify api """
        shopify.ShopifyResource.activate_session(shopify_session)

        current_shop = shopify.Shop.current()

        domain_parts = current_shop.__dict__['attributes']['domain'].split('.')

        shop, is_new = self.get_or_create(shopify_id=current_shop.id )
        shop.data = current_shop.__dict__['attributes']
        shop.save()

        return shop

    def get_or_create_user(self, shop):
        """ Get/Create the user for this Shop 
        depending if it exists or not """
        name = shop.data['shop_owner']
        first_name = name.split(' ')[0]
        last_name = ' '.join(name.split(' ')[1:])
        unique_id = '%d-%s' %(shop.data['id'], name,)
        username = slugify(unique_id)
        email = shop.data['email']
        user, is_new = User.objects.get_or_create(username=username, email=email, first_name=first_name, last_name=last_name)
        if is_new or not shop.users.filter(pk=user.pk).exists():
            shop.users.add(user)
        return user

    def create_webhook_if_not_exists(self, request):
        """ Create the webhook on the remote app if it does not exist """
        webhook_callback_address = request.build_absolute_uri(reverse('webhook:invite_review_create'))
        webhook = shopify.Webhook.find(address=webhook_callback_address)

        if not webhook:
            # Create it
            new_webhook = shopify.Webhook()
            new_webhook.topic = 'orders/create'
            new_webhook.address = webhook_callback_address
            new_webhook.format = 'json'
            new_webhook.save()

            # Try to get the newly created webhook again
            webhook = shopify.Webhook.find(address=webhook_callback_address)
            if not webhook:
                # no luck is probably the host
                raise ImproperlyConfigured('Suspect that %s is not allowed by remote host' %(webhook_callback_address,))

        return webhook

