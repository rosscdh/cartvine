from django.db import models
from jsonfield import JSONField
from shop_happy.apps.shop.models import Shop


class Customer(models.Model):
    shops = models.ManyToManyField(Shop, related_name='shops')
    shopify_id = models.IntegerField(db_index=True, null=True, blank=True)
    first_name = models.CharField(max_length=128, null=True, blank=True)
    last_name = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField()
    data = JSONField(null=True)

    def __unicode__(self):
        return u'%s - %s' % (self.get_full_name, self.email, )

    @property
    def get_full_name(self):
        return u'%s %s' % (self.first_name, self.last_name, )

    @property
    def shopify_updated_at(self):
        return self.data['updated_at'] if 'updated_at' in self.data and not None else None

