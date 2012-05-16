from celery.task import task

from shop_happy.apps.shop.models import Shop
from django.template.defaultfilters import slugify

from models import Webhook

import shopify


@task(name="sync_webhook",retries=2)
def sync_webhook(webhook_callback_address, shop, shopify_session):
    """ Task to sync the products listed in Shopify shop with local database 
    Called on login/install """
    shopify.ShopifyResource.activate_session(shopify_session)

    Webhook.objects.create_webhook_if_not_exists(webhook_callback_address, shop)

    return None

