from django.conf import settings
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from urlparse import urlparse

from cartvine.apps.widget.models import Widget, WidgetInfo, WidgetShop


register = template.Library()


@register.assignment_tag(takes_context=True)
def widget_details(context):
    """
    Return the appropriate WidgetInfo object according to request users plan
    """
    details_list = WidgetInfo.objects.filter(widget=context['object'])
    details = {'summary': '', 'detail': '' }
    for d in details_list:
        if d.plan.slug == 'basic':
            details['summary'] = d.summary
            details['detail'] = d.info
            break
    return details
widget_details.is_safe = True
