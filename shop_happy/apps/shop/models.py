from django.db import models
from django.contrib.auth.models import User

from shop_happy.fields import JSONField
from managers import ShopManager

class Shop(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name='users')
    shopify_id = models.IntegerField(db_index=True)
    slug = models.SlugField(db_index=True)
    url = models.URLField()
    data = JSONField(null=True)

    objects = ShopManager()

    def __unicode__(self):
        return u'%s - %d' % (self.slug, self.shopify_id,)

