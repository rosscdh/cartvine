import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__+ '/../'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stard0g101_cvine',
        'USER': 'stard0g101_cvine',
        'PASSWORD': '90aa508a',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

STATIC_URL = '/static/cartvine/'

STATIC_ROOT = '/home/stard0g101/webapps/static/cartvine/'

# Additional locations of static files
STATICFILES_DIRS = (
    '/home/stard0g101/webapps/static/cartvine/base/',
)

# Shopify Key
SHOPIFY_API_KEY = '44af80f89180e77316223733d99bf8c7'
SHOPIFY_API_SECRET = '0ee7abaeade2098cec4c8e2bf3770fe8'

#Facebook App Id
FACEBOOK_APP_ID = '209234305864956'

