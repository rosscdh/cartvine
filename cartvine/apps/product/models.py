from django.db import models
from django.template.defaultfilters import slugify

from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.dispatch import receiver

import colorsys
import webcolors

from jsonfield import JSONField
from cartvine.utils import get_namedtuple_choices, DictDiffer
from cartvine.apps.shop.models import Shop

from signals import add_variant_property, delete_variant_property

from managers import ProductManager


def get_property_dict(**kwargs):
    return {"option_id": kwargs['option_id'], "slug": slugify(kwargs['name']), "name": kwargs['name'], "value": kwargs['value']}

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

    def get_images_src(self):
        return self.data['images'] if 'images' in self.data and isinstance(self.data['images'], type([])) else None

# ----- PROPERTY METHODS -----
    def compile_basic_properties_from_variants(self, variant_list):
        """ @KEYMETHOD """
        for v in variant_list:
            for option_id,basic_option in Product.BASIC_OPTIONS.get_choices():
                self.set_property(option_id=option_id, value=v[option_id])

    def valid_properties_list(self):
        if 'all_properties' not in self.data or type(self.data['all_properties']) != type([]):
            return False
        else:
            return True

    def ensure_all_properties(self):
        if not self.valid_properties_list():
            self.set_data_all_properties()

    def all_properties(self):
        self.ensure_all_properties()
        return self.data['all_properties']

    def set_data_all_properties(self):
        self.data['all_properties'] = []

    def ensure_option_id(self, option_id=None):
        if option_id in [None,'',False]:
            option_id = self.get_next_properties_plus_option_id()
        return option_id

    def set_property(self, option_id=None, value=None):
        found = False

        option_id = self.ensure_option_id(option_id)

        for i,p in enumerate(self.all_properties()):
            if p['option_id'] == option_id:
                p['name'] = value # This is the important line .. in Property name==value and in Variant value==value
                self.data['all_properties'][i] = p
                found = True
                break

        if found is False:
            new_property = get_property_dict(option_id=option_id, name=value, value=None)
            self.data['all_properties'].append(new_property)
            # Add property to variants signal
            add_variant_property.send(sender=self, user_id=1, new_property=new_property)

        return found

    def delete_property(self, option_id):
        for i,p in enumerate(self.all_properties()):
            if p['option_id'] == option_id:
                del(self.data['all_properties'][i])
                # Delete property from variants signal
                delete_variant_property.send(sender=self, user_id=1, option_id=option_id)

    def basic_properties(self, options=None):
        """ @KEYMETHOD """
        basic_properties = dict({})
        options = [option_id for option_id,v in self.BASIC_OPTIONS.get_choices()]

        for p in self.all_properties():
            if p['option_id'] in options:
                basic_properties[p['option_id']] = {'slug': p['slug'], 'name': p['name'],}

        return [(key, basic_properties[key]) for key in sorted(basic_properties.iterkeys())]

    def plus_properties(self, options=None):
        """ @KEYMETHOD """
        plus_properties = dict({})
        options = [option_id for option_id,v in self.BASIC_OPTIONS.get_choices()]

        for p in self.all_properties():
            if p['option_id'] not in options:
                plus_properties[p['option_id']] = {'slug': p['slug'], 'name': p['name'],}

        return [(key, plus_properties[key]) for key in sorted(plus_properties.iterkeys())]

    def get_next_properties_plus_option_id(self):
        if not self.valid_properties_list():
            index = 1
        else:
            index = len(self.all_properties()) + 1
        return 'option%d' %(index,)

    def property_colors(self):
        props = self.plus_properties()
        num_props = len(props)
        colors = {}
        if num_props > 0:
            crange = get_color_range(num_props)
            c = 0
            for k,v in props:
                colors[k] = crange[c]
                c = c+1
        return colors
# ----- END PROPERTY METHODS -----

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

    def __unicode__(self):
        return u'%s' %(self.sku)

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
        self.ensure_all_properties()
        for option_id,o in Product.BASIC_OPTIONS.get_choices():
            for o in self.data['all_properties']:
                if option_id == o['option_id']:
                    options[option_id] = o['value'] if hasattr(o,'value') else None
        return [(key, options[key]) for key in sorted(options.iterkeys())]

    def set_property(self, option_id=None, value=None):
        found = False

        option_id = self.product.ensure_option_id(option_id)

        self.ensure_all_properties()

        for i,p in enumerate(self.product.all_properties()):
            if p['option_id'] == option_id:
                p['value'] = value

                try:
                    self.data['all_properties'][i] = p
                except IndexError:
                    self.data['all_properties'].append(p)

                found = True
                break

        if found is False:
            new_property = get_property_dict(option_id=option_id, name=None, value=value)
            self.data['all_properties'].append(new_property)
        return found

    def ensure_all_properties(self):
        if 'all_properties' not in self.data or type(self.data['all_properties']) != type([]):
            self.set_data_all_properties()

    def all_properties(self):
        self.ensure_all_properties()
        return self.data['all_properties']

    def set_data_all_properties(self, properties=None):
        if properties is None:
            properties = self.product.all_properties()
        self.data['all_properties'] = properties




# ----- Recievers -----

@receiver(add_variant_property)
def new_variant_property(sender, **kwargs):
    user_id = kwargs['user_id']
    product_property = kwargs['new_property']
    variant_list = sender.productvariant_set.all()
    num_variants = len(variant_list)
    for v in variant_list:
        found = False
        props = v.all_properties()
        for i,p in enumerate(props):
            if p['option_id'] == product_property['option_id']:
                found = True
                break
        if found is False:
            new_property = get_property_dict(option_id=product_property['option_id'], name=product_property['name'], value=None)
            v.data['all_properties'].append(new_property)
            v.save()
    change_message = 'Added a new Property "%s" for %d Variants for Product - %s' %(product_property['name'], num_variants, sender.name,)
    LogEntry.objects.log_action(user_id, ContentType.objects.get_for_model(sender).pk, sender.pk, force_unicode(sender), ADDITION, change_message)


@receiver(delete_variant_property)
def del_variant_property(sender, **kwargs):
    user_id = kwargs['user_id']
    option_id = kwargs['option_id']
    option_name = None
    variant_list = sender.productvariant_set.all()
    num_variants = len(variant_list)
    for v in variant_list:
        props = v.all_properties()
        for i,p in enumerate(props):
            if p['option_id'] == option_id:
                option_name = p['name']
                del(props[i])
        v.set_data_all_properties(props)
        v.save()
    print("delete_variant_property Request finished!")
    change_message = 'Deleted Property "%s" for %d Variants for Product - %s' %(option_name, num_variants, sender.name,)
    LogEntry.objects.log_action(user_id, ContentType.objects.get_for_model(sender).pk, sender.pk, force_unicode(sender), DELETION, change_message)

