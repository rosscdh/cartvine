from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from shop_happy.fields import JSONField
from shop_happy.apps.shop.models import Shop
from managers import WebhookManager


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

    objects = WebhookManager()

    def __unicode__(self):
        return u'%s - %d' % (self.topic, self.shopify_id,)

