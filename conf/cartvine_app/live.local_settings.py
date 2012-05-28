import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__+ '/../'))

SITE_ID = 1

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
SHOPIFY_API_KEY = '5a9dbf6950f6f4719a226e4f32276dca'
SHOPIFY_API_SECRET = 'faba2795c9cf719949c8c7d5b4a1bd9e'

#Facebook App Id
FACEBOOK_APP_ID = '209234305864956'
FACEBOOK_APP_SECRET = '8a2b5757c513965faff0de2c35dcdbf2'
