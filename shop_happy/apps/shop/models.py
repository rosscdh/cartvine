from django.db import models
from shop_happy.fields import JSONField


class Shop(models.Model):
    name = models.CharField(max_length=255)
    shopify_id = models.IntegerField()
    slug = models.SlugField()
    url = models.URLField()
    data = JSONField(null=True)

