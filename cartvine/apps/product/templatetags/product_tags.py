from django.conf import settings
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify
from urlparse import urlparse

from cartvine.utils import get_namedtuple_choices
from cartvine.apps.product.models import Product

import re


register = template.Library()

SHOP_IMAGE_SIZE = get_namedtuple_choices('SHOP_IMAGE_SIZE', (
    ('pico', 'pico', 'Pico'),
    ('icon', 'icon', 'Icon'),
    ('thumb', 'thumb', 'Thumbnail'),
    ('small', 'small', 'Small'),
    ('compact', 'compact', 'Compact'),
    ('medium', 'medium', 'Medium'),
    ('large', 'large', 'Large'),
    ('grande', 'grande', 'Grande'),
    ('original', 'original', 'Original'),
))

@register.filter
def image_resize(src, size=None):
    """
    Reformat the image name to have <image_name>_SIZE.jpg in it
    """
    if size not in SHOP_IMAGE_SIZE.get_values():
        size = SHOP_IMAGE_SIZE.compact

    image = urlparse(src)
    path = image.path.split('.')
    path = '%s_%s.%s' % (path[0],size,path[1],)
    #@TODO what is the filterspec? last value of the urlparse object?
    a,b,c,d,e,f = image
    return '%s://%s%s?%s%s' %(image.scheme, image.netloc, path, image.params, e)
image_resize.is_safe = True


@register.filter
def option_offset(option):
    non_decimal = re.compile(r'[^\d]+')
    num = non_decimal.sub('', option)
    return 'option%d' %(int(num) + Product.OPTION_OFFSET)
option_offset.is_safe = True

@register.filter
def option_color(option_id):
    return '%s' % (Product.OPTION_COLORS.get_value_by_name(option_id),)
option_color.is_safe = True


@register.filter
def color_plus(option_id):
    return '%s' %('none',)    
color_plus.is_safe = True


@register.inclusion_tag('product/partials/product_properties.html')
def all_product_properties_script(shop, product):
    property_list = {}
    found_items = {}
    for product in Product.objects.by_shop(shop).exclude(pk=product.pk).all():
        for p in product.all_properties():
            slug = slugify(p['name'])
            p['slug'] = slug
            # initializers
            if p['option_id'] not in property_list:
                property_list[p['option_id']] = []
                found_items[p['option_id']] = []

            # make it a unique list
            if slug not in found_items[p['option_id']]:
                found_items[p['option_id']].append(slug)
                if p['name'] not in [None,'','None']:
                    property_list[p['option_id']].append(p)


    return {'property_list': property_list}
all_product_properties_script.is_safe = True
