from django.db import models
from shop_happy.apps.shop.models import Shop


class Customer(models.Model):
    shops = models.ManyToManyField(Shop, related_name='shops')
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField()
