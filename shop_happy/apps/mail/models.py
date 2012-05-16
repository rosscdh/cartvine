from django.db import models
from shop_happy.apps.shop.models import Shop
from shop_happy.apps.customer.models import Customer


class Email(models.Model):
    shop = models.ForeignKey(Shop)
    customer = models.ForeignKey(Customer, related_name='target_customer')
    email_to = models.EmailField()
    body = models.TextField()