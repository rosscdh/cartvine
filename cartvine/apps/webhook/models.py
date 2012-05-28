from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from jsonfield import JSONField

from cartvine.utils import get_namedtuple_choices
from cartvine.apps.shop.models import Shop



class Webhook(models.Model):
    TOPICS = (
        (0, _('orders/create')),
        # there are more
    )
    FORMATS = (
        ('xml', _('xml')),
        ('json', _('json')),
    )
    shop = models.ForeignKey(Shop)
    shopify_id = models.IntegerField(db_index=True)
    topic = models.CharField(max_length=64)
    address = models.URLField(max_length=255)
    format = models.CharField(max_length=6,choices=FORMATS)

    def __unicode__(self):
        return u'%s - %d' % (self.topic, self.shopify_id,)


class OrderCreatePostback(models.Model):
    """ Model to store postbacks Created on order/create Webhook calls """
    shop = models.ForeignKey(Shop)
    shop_url = models.CharField(max_length=255,null=True)
    content_type = models.CharField(max_length=255,null=True)
    date_recieved = models.DateTimeField(auto_now=True, auto_now_add=True)
    recieved_from = models.CharField(max_length=255, null=True, blank=True)
    recieved_from_ip = models.IPAddressField()
    data = JSONField()

    class Meta:
        ordering = ['-pk']

    def __unicode__(self):
        return u'%s - %s (%s)' % (self.shop_url, self.date_recieved, self.recieved_from_ip)

    def get_order_products(self):
        return self.data['line_items']