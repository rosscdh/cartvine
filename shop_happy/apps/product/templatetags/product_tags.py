from django.conf import settings
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from urlparse import urlparse
from shop_happy.utils import get_namedtuple_choices

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
    src = '%s://%s%s?%s%s' %(image.scheme, image.netloc, path, image.params, e)
    return src
image_resize.is_safe = True
