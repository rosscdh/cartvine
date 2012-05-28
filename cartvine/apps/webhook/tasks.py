from celery.task import task
from django.conf import settings
from cartvine.apps.shop.models import Shop
from django.template.defaultfilters import slugify

from models import Webhook

import shopify
import logging
logger = logging.getLogger('happy_log')


@task(name="sync_shopify_webhook")
def sync_webhook(webhook_callback_address, shop, shopify_session):
    """ Task to sync the products listed in Shopify shop with local database 
    Called on login/install """

    shop.activate_shopify_session()

    webhook = shopify.Webhook.find(address=webhook_callback_address)

    if not webhook:
        # Create it
        logger.info('No Shopify Webhook found for %s %s'%(shop,webhook_callback_address,))

        new_webhook = shopify.Webhook()
        new_webhook.topic = 'orders/create'
        new_webhook.address = webhook_callback_address
        new_webhook.format = 'json'
        new_webhook.save()

        # Try to get the newly created webhook again
        webhook = shopify.Webhook.find(address=webhook_callback_address)

    if webhook:
        webhook = webhook[0]
        webhook, is_new = Webhook.objects.get_or_create(shop=shop, shopify_id=webhook.id, topic=webhook.topic, address=webhook.address, format=webhook.format)
        if is_new:
            logger.info('Created Shopify Webhook and Local Webhook for %s %s'%(shop,webhook_callback_address,))
    else:
        # no luck is probably the host
        logger.error('Could not create Shopify Webhook %s %s - Suspect that %s is not a valid postback hot and is refused by shopify'%(shop,webhook_callback_address,webhook_callback_address,))

    return None

