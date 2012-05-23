from celery.task import task

from shop_happy.apps.shop.models import Shop
from django.template.defaultfilters import slugify

from models import Customer

import shopify
import logging
logger = logging.getLogger('happy_log')


@task(name="sync_customers")
def sync_customers(shopify_session, shop):
    """ Task to sync the products listed in Shopify shop with local database 
    Called on login/install """

    shop.activate_shopify_session()

    try:
        latest_customer = Customer.objects.filter(shops__pk__in=[shop.pk]).latest('pk')
    except Customer.DoesNotExist:
        # No Customers stored locally so simple get them all from the shop
        logger.info('No Customers stored locally for %s so get all from the Shopify API'%(shop,))
        latest_customer = None
        shopify_customers = shopify.Customer.find()

    if latest_customer:
        shopify_customers = shopify.Customer.find(since_id=latest_customer.shopify_id)
        if latest_customer.shopify_updated_at:
            shopify_customers += shopify.Customer.find(updated_at_min=latest_customer.shopify_updated_at)

    if shopify_customers:
        logger.info('%d new Customers found for %s'%(len(shopify_customers),shop,))
        for customer in shopify_customers:
            # should use get_or_create here?
            safe_attribs = customer.__dict__['attributes']
            safe_attribs['addresses'] = None

            c, is_new = Customer.objects.get_or_create(shopify_id=customer.id)
            c.first_name = customer.first_name
            c.last_name = customer.last_name
            c.email = customer.email
            c.data = safe_attribs
            c.save()
            # Add the current shop to the customer
            if shop not in c.shops.all():
                c.shops.add(shop)

    return None
