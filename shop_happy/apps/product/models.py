from django.db import models
from shop_happy.fields import JSONField

from shop_happy.apps.shop.models import Shop


class Product(models.Model):
    shop = models.ForeignKey(Shop)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    data = JSONField()
