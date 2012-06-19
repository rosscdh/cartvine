from django.db import models
from django.template.defaultfilters import slugify

import numpy as np
import colorsys

from jsonfield import JSONField
from cartvine.utils import get_namedtuple_choices
from cartvine.apps.shop.models import Shop
from managers import ProductManager


def _get_colors(num_colors):
    colors=[]
    if num_colors > 0:
        for i in np.arange(0., 360., 360. / num_colors):
            hue = i/360.
            lightness = (50 + np.random.rand() * 10)/100.
            saturation = (90 + np.random.rand() * 10)/100.
            colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
    return colors


class Product(models.Model):
    OPTION_OFFSET = 3 # offset fromwhich to start the plus property counter
    PROPERTY_TYPE = get_namedtuple_choices('PROPERTY_TYPE', (
        (0, 'base', 'Base Attributes'),
        (1, 'basic', 'Basic Properties'),
        (2, 'plus', 'PropertiesPlus'),
    ))
    BASIC_OPTIONS = get_namedtuple_choices('BASIC_OPTIONS', (
        ('option1', 'option1', 'Option 1'),
        ('option2', 'option2', 'Option 2'),
        ('option3', 'option3', 'Option 3'),
    ))
    OPTION_COLORS = get_namedtuple_choices('OPTION_COLORS', (
        ('#237FAD', 'option1', 'Option 1'),
        ('#7EA336', 'option2', 'Option 2'),
        ('#A95A05', 'option3', 'Option 3'),
    ))
    shop = models.ForeignKey(Shop)
    provider_id = models.IntegerField(db_index=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    data = JSONField()

    objects = ProductManager()

    def __unicode__(self):
        return u'%s' % (self.slug,)

    @property
    def summary(self):
        return u'%s' % (self.data['body_html'],)

    @property
    def product_type(self):
        return u'%s' % (self.data['product_type'],)

    @property
    def shopify_url(self):
        return u'/admin/products/%d' % (self.provider_id,)

    @property
    def shopify_updated_at(self):
        return self.data['updated_at'] if 'updated_at' in self.data and self.data['updated_at'] is not None else None

    @property
    def featured_image_src(self):
        return self.data['featured_image'] if 'featured_image' in self.data and self.data['featured_image'] is not None else None

    def tags(self):
        return self.data['tags'].split() if 'tags' in self.data and self.data['tags'] is not None else None

    def get_variant_prop_groups(self, options=None):
        if options is None:
            options = {}
        #assemble variant options
        for v in self.data['variants']:
            for option_id,o in self.BASIC_OPTIONS.get_choices():
                if option_id not in options:
                    options[option_id] = {'name':option_id, 'value': [v[option_id]]}
                else:
                    options[option_id]['value'].append(v[option_id])
        return options

    def get_data_options(self, options=None):
        if options is None:
            options = {}
            for option_id,o in self.BASIC_OPTIONS.get_choices():
                options[option_id] = {'name':'', 'value':''}

        for i,o in enumerate(self.data['options']):
            option_id = 'option%s'%(i+1,)
            options[option_id]['name'] = o['name']
            options[option_id]['value'] = set(options[option_id]['value'])
        return options

    def basic_props(self):
        """ assemble properties and lis of variant options uniquified ordered by name.. option1 option2... """
        basic = []
        options = self.get_data_options(self.get_variant_prop_groups())
        for option_id,name in self.BASIC_OPTIONS.get_choices():
            p = options[option_id]
            # append the id to the p object
            p['option_id'] = option_id
            basic.append(p)
        return basic

    @property
    def has_properties_plus(self):
        return True if 'properties_plus' in self.data else False

    def reset_properties_plus(self):
        self.data['properties_plus'] = {}

    def get_next_properties_plus_option_id(self):
        if not self.has_properties_plus:
            index = 1
        else:
            index = len(self.data['properties_plus']) + 1
        return 'option%d' %(index,)

    def set_properties_plus(self, value, option_id=None):
        if not self.has_properties_plus:
            self.reset_properties_plus()

        if option_id in [None,'']:
            option_id = self.get_next_properties_plus_option_id()

        self.data['properties_plus'][option_id] = value

    def properties_plus(self):
        return [] if not self.has_properties_plus else [(key, self.data['properties_plus'][key]) for key in sorted(self.data['properties_plus'].iterkeys())]

    def properties_plus_colors(self):
        props = self.properties_plus()
        colors = _get_colors(len(props))
        c = 0
        for k,v in props:
            props[k] = colors[c]
            c = c+1
        return props


    def get_images_src(self):
        return self.data['images'] if 'images' in self.data and isinstance(self.data['images'], type([])) else None


class ProductVariant(models.Model):
    product = models.ForeignKey(Product)
    slug = models.SlugField(null=True)
    provider_id = models.IntegerField(null=True,db_index=True)
    sku = models.CharField(max_length=128,null=True,db_index=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    inventory_quantity = models.IntegerField(default=0)
    position = models.IntegerField(default=0)
    data = JSONField()

    class Meta:
        ordering = ['position']

    def set_slug(self):
        if 'extra_options' in self.data:
            for i in self.data['extra_options']:
                pass
        #self.slug = slugify()

    @property
    def cost(self):
        return u'%s' %(self.data['price'] if 'price' in self.data else 0,)

    @property
    def weight_as_kg(self):
        return '%d' %(self.data['grams'] if 'grams' in self.data else 0,)

    def basic_options(self):
        options = {}
        for option_id,o in Product.BASIC_OPTIONS.get_choices():
            if option_id in self.data:
                options[option_id] = {'name':option_id, 'value': self.data[option_id]}
        return options
