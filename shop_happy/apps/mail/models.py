from django.db import models
from shop_happy.apps.shop.models import Shop
from shop_happy.apps.customer.models import Customer

from managers import ShopHappyEmailManager

import datetime


class ShopHappyEmail(models.Model):
    shop = models.ForeignKey(Shop)
    customer = models.ForeignKey(Customer, related_name='target_customer')
    email_to = models.EmailField()
    post_date = models.DateField()
    sent_date = models.DateField(null=True,blank=True)
    body = models.TextField()

    objects = ShopHappyEmailManager()
