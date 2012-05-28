from django.db import models
from django.template import loader

from cartvine.apps.shop.models import Shop
from cartvine.apps.customer.models import Customer


import logging
logger = logging.getLogger('happy_log')


class ShopHappyEmailManager(models.Manager):

    def create_email_from_callback(self, callback_order):
        """ Create an email record form the webhook order """
        logger.info('Setting Callback Order: %s'%(callback_order,))

        customer, is_new = Customer.objects.get_or_create(email=callback_order.data['customer']['email'], first_name=callback_order.data['customer']['first_name'], last_name=callback_order.data['customer']['last_name'])

        email_to = callback_order.data['customer']['email']
        data = {'customer': callback_order.data['customer'], 'line_items': callback_order.data['line_items']}
        post_date = self.model.get_email_post_date()

        email = self.create(shop=callback_order.shop, customer=customer, post_date=post_date, email_to=email_to, data=data)
        return email
