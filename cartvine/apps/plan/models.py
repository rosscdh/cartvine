from django.db import models
from django.contrib.auth.models import User

from jsonfield import JSONField
from cartvine.utils import get_namedtuple_choices


class Plan(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField()
    data = JSONField(null=True)

    def __unicode__(self):
        return u'%s'%(self.name,)
