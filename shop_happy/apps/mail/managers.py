from django.db import models
from django.template import loader

from shop_happy.apps.shop.models import Shop
from shop_happy.apps.customer.models import Customer

import logging
logger = logging.getLogger('happy_log')


class ShopHappyEmailManager(models.Manager):

    def create_email_from_callback(self, callback_order):
        """ Create an email record form the webhook order """
        logger.info('Setting Callback Order: %s'%(callback_order,))

        shop_url = 'http://%s' %(callback_order.shop_name,) #@TODO move to shop manager and make it a method

        shop = Shop.objects.get(url=shop_url)

        post_date = Shop.get_email_post_date()
        customer, is_new = Customer.objects.get_or_create(email=callback_order.data['customer']['email'], first_name=callback_order.data['customer']['first_name'], last_name=callback_order.data['customer']['last_name'])
        email_to = callback_order.data['customer']['email']
        # Load template
        body = loader.render_to_string('mail/invitation_to_review.html', {
            'shop': shop,
            'name': customer.get_full_name,
            'product_list': callback_order.get_order_products(),
        })

        email = self.create(shop=shop, customer=customer, post_date=post_date, email_to=email_to, body=body)
        return email
