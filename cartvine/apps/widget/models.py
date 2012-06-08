from django.db import models
from django.conf import settings
from jsonfield import JSONField
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from cartvine.utils import get_namedtuple_choices
from cartvine.apps.plan.models import Plan
from cartvine.apps.shop.models import Shop


class Widget(models.Model):
    """ Widgets Purchased by a Shop """
    WIDGET_TYPE = get_namedtuple_choices('WIDGET_TYPE', (
        ('js', 'text_javascript', 'Javascript'),
        ('app', 'application', 'Application'),
    ))
    name = models.CharField(max_length=128)
    widget_type = models.CharField(max_length=5, choices=WIDGET_TYPE.get_choices())
    slug = models.SlugField()
    data = JSONField(null=True,default='{"templates": [""], "icons": {"widget_list": ""}}')
    is_active = models.BooleanField(default=True,null=False)
    shop = models.ManyToManyField(Shop, through='WidgetShop')
    info = models.ManyToManyField(Plan, through='WidgetInfo')

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name,)

    @property
    def widget_list_image(self):
        if 'icons' in self.data and 'widget_list' in self.data['icons']:
            return '%s' % (self.data['icons']['widget_list'],)
        else:
            return None

    @property
    def widget_js_name(self):
        return u'%s' %(self.slug.replace('-','_'))


class WidgetInfo(models.Model):
    """ Modle used to store the Widget Description Info """
    widget = models.ForeignKey(Widget)
    plan = models.ForeignKey(Plan)
    summary = models.CharField(max_length=255,blank=True,help_text=_('Please use only Markdown here'))
    info = models.TextField(blank=True,help_text=_('Please use only Markdown here'))

    class Meta:
        ordering = ['widget__name', 'plan']
        verbose_name = 'Widget Info'
        verbose_name_plural = 'Widget Info'

    def __unicode__(self):
        return u'%s - %s' % (self.widget.name, self.plan,)


class WidgetShop(models.Model):
    """ Overriden join table so we can store widget settings """
    widget = models.ForeignKey(Widget)
    shop = models.ForeignKey(Shop)
    is_active = models.BooleanField(default=True,null=False)
    data = JSONField(null=True,default='{"target_id": "body"}')

    class Meta:
        db_table = 'widget_widget_shop'
        verbose_name = _('Per Shop Config')
        verbose_name_plural = 'Per Shop Config'
