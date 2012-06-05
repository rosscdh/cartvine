from celery.task import task

from django.template.defaultfilters import slugify
from django.template import loader, Context
from django.contrib.sites.models import Site

from cartvine.apps.shop.models import Shop
from models import Widget, WidgetShop

import shopify
from pyactiveresource.connection import ResourceNotFound
import logging
logger = logging.getLogger('happy_log')


@task(name="sync_assets")
def sync_assets(shop):
    """ Task to sync the assets installed on the remote client with 
    Ours """
    site_list = Site.objects.all()

    c = Context()
    c['shopify_app_domain'] = site_list[0].domain
    c['shoppers_app_domain'] = site_list[1].domain

    key = 'assets/cartvine-loader.js'
    loader_script = loader.get_template('widget/cartvine-loader.js').render(c)

    shop.activate_shopify_session()
    try:
        cartvineloader_asset = shopify.Asset.find(key=key)
    except ResourceNotFound:
        # not present so create it
        cartvineloader_asset = shopify.Asset()
        cartvineloader_asset.key = key

    cartvineloader_asset.value = loader_script
    cartvineloader_asset.save()
    logger.info('Updated Shopify Asset cartvine-loader.js %s'%(shop,))

    return None
