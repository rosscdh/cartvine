from celery.task import task

from shop_happy.apps.shop.models import Shop
from django.template.defaultfilters import slugify

from models import Webhook

import shopify


@task
def sync_webhook(request, shop, shopify_session):
    """ Task to sync the products listed in Shopify shop with local database 
    Called on login/install """

    shopify.ShopifyResource.activate_session(shopify_session)

    return Webhook.objects.create_webhook_if_not_exists(request, shop)

