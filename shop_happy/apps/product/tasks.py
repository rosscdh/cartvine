from celery.task import task

from shop_happy.apps.shop.models import Shop
from django.template.defaultfilters import slugify

from models import Product

import shopify


@task(name="sync_products")
def sync_products(shopify_session, shop):
    """ Task to sync the products listed in Shopify shop with local database 
    Called on login/install """

    shopify.ShopifyResource.activate_session(shopify_session)

    try:
        latest_product = Product.objects.filter(shop=shop).latest('shopify_id')
    except Product.DoesNotExist:
        # No Products stored locally so simple get them all from the shop
        latest_product = None
        shopify_products = shopify.Product.find()

    if latest_product:
        shopify_products = shopify.Product.find(since_id=latest_product.shopify_id)

    if shopify_products:
        for product in shopify_products:
            # should use get_or_create here?
            safe_attribs = product.__dict__['attributes']
            safe_attribs['variants'] = None
            safe_attribs['options'] = None
            safe_attribs['featured_image'] = product.images[0].src if product.images else None
            p, is_new = Product.objects.get_or_create(shop=shop, shopify_id=product.id, name=product.title, slug=slugify(product.title), data=safe_attribs)
            if not is_new:
                p.data = safe_attribs
            p.save()

    return None

