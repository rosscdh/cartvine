import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__+ '/../'))

STATIC_URL = '/static/cartvine/'

STATIC_ROOT = '/home/stard0g101/webapps/static/cartvine/'

# Additional locations of static files
STATICFILES_DIRS = (
    '/home/stard0g101/webapps/static/cartvine/base/',
)

# Shopify Key
SHOPIFY_API_KEY = '44af80f89180e77316223733d99bf8c7'
SHOPIFY_API_SECRET = '0ee7abaeade2098cec4c8e2bf3770fe8'
