from django.db import models
from shop_happy.fields import JSONField


class Shop(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)
    slug = models.SlugField(null=True)
    url = models.URLField(null=False, blank=False)
    data = JSONField(null=True)

