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
    data = JSONField()
    shop = models.ManyToManyField(Shop, through='WidgetShop')

    def __unicode__(self):
        return u'%s' % (self.name,)


class WidgetShop(models.Model):
    """ Overriden join table so we can store widget settings """
    widget = models.ForeignKey(Widget)
    shop = models.ForeignKey(Shop)
    data = JSONField(null=True)
    class Meta:
        db_table = 'widget_widget_shop'
        verbose_name = _('Widget Configuration')
        verbose_name_plural = 'Widget Configuration'
