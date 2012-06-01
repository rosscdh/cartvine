from django.db import models
from django.contrib.auth.models import User

from jsonfield import JSONField
from managers import ShopManager

import shopify
import datetime


class Shop(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name='users')
    provider_id = models.IntegerField(db_index=True)
    provider_access_token = models.CharField(max_length=255,db_index=True)
    slug = models.SlugField(db_index=True)
    url = models.URLField(db_index=True)
    data = JSONField(null=True)

    objects = ShopManager()

    def __unicode__(self):
        return u'%s - %d' % (self.slug, self.provider_id,)

    def activate_shopify_session(self):
        """ Activate the shopify session """
        session = shopify.Session(self.url)
        session.token = self.provider_access_token
        return shopify.ShopifyResource.activate_session(session)

