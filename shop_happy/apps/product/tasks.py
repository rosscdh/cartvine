from celery.task import task

from shop_happy.apps.shop.models import Shop
from django.template.defaultfilters import slugify

from models import Product

import shopify


@task
def sync_products(shopify_session, shop):
    """ Task to sync the products listed in Shopify shop with local database 
    Called on login/install """

    shopify.ShopifyResource.activate_session(shopify_session)

    try:
        latest_product = Product.objects.filter(shop=shop).latest('pk')
    except Product.DoesNotExist:
        # No Products stored locally so simple get them all from the shop
        latest_product = None

    if latest_product:
        shopify_products = shopify.Product.find(since=latest_product.shopify_id)
    else:
        shopify_products = shopify.Product.find()

    for product in shopify_products:
        # should use get_or_create here?
        safe_attribs = product.__dict__['attributes']
        safe_attribs['variants'] = None
        safe_attribs['options'] = None
        p = Product(shop=shop, shopify_id=product.id, name=product.title, slug=slugify(product.title), data=safe_attribs)
        p.save()

    return None

