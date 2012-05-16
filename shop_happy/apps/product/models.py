from django.db import models
from shop_happy.fields import JSONField

from shop_happy.apps.shop.models import Shop
from managers import ProductManager


class Product(models.Model):
    shop = models.ForeignKey(Shop)
    shopify_id = models.IntegerField(db_index=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    data = JSONField()

    objects = ProductManager()

    def __unicode__(self):
        return u'%s' % (self.slug,)

    @property
    def shopify_url(self):
        return u'http://%s' % (self.shopify_id,)