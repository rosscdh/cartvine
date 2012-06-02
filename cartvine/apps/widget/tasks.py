from celery.task import task

from cartvine.apps.shop.models import Shop
from django.template.defaultfilters import slugify

from models import Widget, WidgetShop

import shopify
import logging
logger = logging.getLogger('happy_log')


@task(name="sync_assets")
def sync_assets(shopify_session, shop):
    """ Task to sync the assets installed on the remote client with 
    Ours """

    shop.activate_shopify_session()


    return None
