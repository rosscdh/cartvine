from django.db import models
from shop_happy.fields import JSONField


class Shop(models.Model):
    name = models.CharField(max_length=255)
    shopify_id = models.IntegerField(db_index=True)
    slug = models.SlugField(db_index=True)
    url = models.URLField()
    data = JSONField(null=True)

