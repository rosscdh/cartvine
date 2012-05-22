from django.conf import settings
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def image_resize(src, size='large'):
    """
    Reformat the image name to have <image_name>_SIZE.jpg in it
    """
    image = src.split('.')
    src = '%s_%s.%s' % (image[0],size,image[1],)
    return src
image_resize.is_safe = True
