from django.db import models
from django.conf import settings
from jsonfield import JSONField
from django.utils.translation import ugettext_lazy as _

from cartvine.utils import get_namedtuple_choices

from cartvine.apps.shop.models import Shop


class Widget(models.Model):
    """ Widgets Purchased by a Shop """
    WIDGET_TYPE = get_namedtuple_choices('WIDGET_TYPE', (
        ('js', 'text_javascript', 'Javascript'),
    ))
    name = models.CharField(max_length=128)
    widget_type = models.CharField(max_length=5, choices=WIDGET_TYPE.get_choices())
    slug = models.SlugField()
    shop = models.ManyToManyField(Shop)
