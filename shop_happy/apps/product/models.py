from django.db import models
from shop_happy.fields import JSONField

from shop_happy.apps.shop.models import Shop


class Product(models.Model):
    shop = models.ForeignKey(Shop)
    shopify_id = models.IntegerField(db_index=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    data = JSONField()
