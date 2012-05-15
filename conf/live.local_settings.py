import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__+ '/../'))

STATIC_URL = '/static/shopify/'

STATIC_ROOT = '/home/stard0g101/webapps/static/shopify'

# Additional locations of static files
STATICFILES_DIRS = (
    '/home/stard0g101/webapps/static/shopify/base/',
)
