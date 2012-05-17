from celery.task import task
from django.conf import settings
from shop_happy.apps.shop.models import Shop
from django.template.defaultfilters import slugify

from models import Webhook

import shopify


@task(name="sync_shopify_webhook")
def sync_webhook(webhook_callback_address, shop, shopify_session):
    """ Task to sync the products listed in Shopify shop with local database 
    Called on login/install """
    shopify.ShopifyResource.activate_session(shopify_session)

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
            if not settings.DEBUG:
                #raise ImproperlyConfigured('Suspect that %s is not allowed by remote host for shop %s' %(webhook_callback_address,shop,))
                pass
        else:
	    	#webhook, is_new = Webhook.objects.create_webhook_if_not_exists(webhook_callback_address, shop)
	    	pass

    return None

