from django.conf import settings
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from urlparse import urlparse

register = template.Library()


@register.filter
def image_resize(src, size='large'):
    """
    Reformat the image name to have <image_name>_SIZE.jpg in it
    """
    image = urlparse(src)
    path = image.path.split('.')
    path = '%s_%s.%s' % (path[0],size,path[1],)
    src = '%s://%s%s?%s' %(image.scheme, image.netloc, path, image.params)
    return src
image_resize.is_safe = True
