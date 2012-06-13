from django.db import models
from jsonfield import JSONField
from cartvine.utils import get_namedtuple_choices

from cartvine.apps.shop.models import Shop
from managers import ProductManager


class Product(models.Model):
    BASIC_OPTIONS = get_namedtuple_choices('BASIC_OPTIONS', (
        ('option1', 'option1', 'Option 1'),
        ('option2', 'option2', 'Option 2'),
        ('option3', 'option3', 'Option 3'),
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
        return self.data['updated_at'] if 'updated_at' in self.data and not None else None

    @property
    def featured_image_src(self):
        return self.data['featured_image'] if 'featured_image' in self.data else None

    def tags(self):
        return self.data['tags'].split() if 'tags' in self.data else None

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
        """ assemble properties and lis of variant options uniquified"""
        basic = []
        options = self.get_data_options(self.get_variant_prop_groups())
        for name, p in options.iteritems():
            basic.append(p)
        return basic

    def properties_plus(self):
        return []

    def get_images_src(self):
        return self.data['images'] if 'images' in self.data and isinstance(self.data['images'], type([])) else None


class ProductVariant(models.Model):
    product = models.ForeignKey(Product)
    provider_id = models.IntegerField(db_index=True)
    sku = models.CharField(max_length=128,null=True,db_index=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    inventory_quantity = models.IntegerField(default=0)
    data = JSONField()

    @property
    def cost(self):
        return u'%s' %(self.data['price'],)

    @property
    def weight_as_kg(self):
        return '%d' %(self.data['grams']/1000)

    @property
    def num_in_stock(self):
        return '%d' %(self.data['inventory_quantity'],)

    def basic_options(self):
        options = {}
        for option_id,o in Product.BASIC_OPTIONS.get_choices():
            options[option_id] = {'name':option_id, 'value': self.data[option_id]}
        return options
