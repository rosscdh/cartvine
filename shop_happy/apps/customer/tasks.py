from celery.task import task

from shop_happy.apps.shop.models import Shop
from django.template.defaultfilters import slugify

from models import Customer

import shopify


@task(name="sync_customers")
def sync_customers(shopify_session, shop):
    """ Task to sync the products listed in Shopify shop with local database 
    Called on login/install """

    shop.activate_shopify_session()

    try:
        latest_customer = Customer.objects.filter(shops__pk__in=[shop.pk]).latest('pk')
    except Customer.DoesNotExist:
        # No Products stored locally so simple get them all from the shop
        latest_customer = None
        shopify_customers = shopify.Customer.find()

    if latest_customer:
        shopify_customers = shopify.Customer.find(since_id=latest_customer.shopify_id)
        

    if shopify_customers:
        for customer in shopify_customers:
            # should use get_or_create here?
            safe_attribs = customer.__dict__['attributes']
            safe_attribs['addresses'] = None
            c = Customer(shopify_id=customer.id, first_name=customer.first_name, last_name=customer.last_name, email=customer.email, data=safe_attribs)
            c.save()
            c.shops.add(shop)

    return None
