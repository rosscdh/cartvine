from django.db import models
from django.template.defaultfilters import slugify

import colorsys
import webcolors

from jsonfield import JSONField
from cartvine.utils import get_namedtuple_choices
from cartvine.apps.shop.models import Shop
from managers import ProductManager


def get_color_range(num_colors):
    colors=[]
    if num_colors > 0:
        start = 0
        stop = 360
        stop_d = 360.
        step = (stop/num_colors)
        increment = 120
        for i in xrange(start, stop, step):
            hue = i/stop_d
            lightness = (50 + increment * 10)/100.
            saturation = (90 + increment * 10)/100.
            color_rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
            color_hex = webcolors.rgb_to_hex(color_rgb)
            colors.append(color_hex)

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
                options[option_id] = None

        if 'options' not in self.data:
            self.data['options'] = options

        for i,o in enumerate(self.data['options']):
            option_id = 'option%s'%(i+1,)
            options[option_id] = o['name']

        return [(key, options[key]) for key in sorted(options.iterkeys())]

    def basic_props(self):
        """ assemble properties and lis of variant options uniquified ordered by name.. option1 option2... """
        basic = []
        options = self.get_data_options(self.get_variant_prop_groups())
        for option_id,name in self.BASIC_OPTIONS.get_choices():
            p = options[option_id]
            # append the id to the p object
            p['option_id'] = option_id
            p['name'] = name
            basic.append(p)
        return basic

    @property
    def has_basic_properties(self):
        return True if 'properties_basic' in self.data else False

    def reset_basic_properties(self):
        self.data['properties_basic'] = {}

    def set_basic_property(self, value, option_id):
        if not self.has_basic_properties:
            self.reset_basic_properties()

        if value != self.data['properties_basic']:
            # is a change so update variants
            pass

        self.data['properties_basic'][option_id] = value

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
        else:
            if option_id not in [None,'']:
                if value != self.data['properties_plus'][option_id]:
                    # is a change, so update variants
                    pass

        if option_id in [None,'']:
            option_id = self.get_next_properties_plus_option_id()

        self.data['properties_plus'][option_id] = value

    def properties_plus(self):
        return [] if not self.has_properties_plus else [(key, self.data['properties_plus'][key]) for key in sorted(self.data['properties_plus'].iterkeys())]

    def properties_plus_colors(self):
        props = self.properties_plus()
        num_props = len(props)
        colors = {}
        if num_props > 0:
            crange = get_color_range(num_props)
            c = 0
            for k,v in props:
                colors[k] = crange[c]
                c = c+1
        return colors

    def all_properties(self):
        props = self.get_data_options() + self.properties_plus()
        return [{'option_id':option_id, 'name':name } for option_id,name in props]

    def set_data_all_properties(self):
        self.data['all_properties'] = self.all_properties()


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
                options[option_id] = self.data[option_id]
        return [(key, options[key]) for key in sorted(options.iterkeys())]

    def all_properties(self):
        return self.product.all_properties()

    def set_data_all_properties(self):
        self.data['all_properties'] = self.all_properties()
