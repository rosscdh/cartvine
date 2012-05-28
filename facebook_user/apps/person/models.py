from django.db import models
from django.contrib.auth.models import User

from jsonfield import JSONField
from cartvine.utils import get_namedtuple_choices

from cartvine.apps.shop.models import Shop


class Person(models.Model):
    # @TODO - Implement this when we get more than 1 app
    APPLICATION_TYPES = get_namedtuple_choices('APPLICATION_TYPES', (
        (1, 'facebook', 'Facebook'),
    ))
    user = models.OneToOneField(User, related_name='person', null=True, blank=True)
    shops = models.ManyToManyField(Shop, null=True, blank=True)
    application_type = models.IntegerField(db_index=True, choices=APPLICATION_TYPES.get_choices())
    uid = models.IntegerField(db_index=True, unique=True)
    access_token = models.CharField(max_length=255, db_index=True)
    data = JSONField(null=True)

    def __unicode__(self):
        return u'%s (%s)'%(self.user, self.uid,)

    def get_validated_json_response(self):
        return {
                'id': self.pk,
                'application_type': self.application_type,
                'uid': self.uid,
                'is_valid': True,
                'user': self.data,
                'shops': [{'id': 1, 'name': 'shop_1'}, ],
                'products': [],
            }