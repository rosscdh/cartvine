import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__+ '/../'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Ross', 'sendrossemail@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(SITE_ROOT, 'dev.db'),
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

USE_ETAGS = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/m/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(STATIC_ROOT, 'base'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+!&amp;e%aq9_qkjbyrneg@h#aum!u)2ug@s!m8vyugzvjvopkk%eq'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    # Facebook Api Key Context Processor
    # 'facebook_user.context_processors.facebook_app_id',
    # Get cartvine sites
    'cartvine.context_processors.cartvine_sites',
    # shopify
    'cartvine.context_processors.current_shop',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Allow Remote Json Requests
    'cartvine.middleware.XsSharing',
    # shopify
    'cartvine.middleware.LoginProtection',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'cartvine.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'cartvine.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

AUTHENTICATION_BACKENDS  = (
    'django.contrib.auth.backends.ModelBackend',
    'cartvine.backends.ShopifyUserBackend',
)

BASE_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.markup',
)


HELPER_APPS = (
    # Addons
    'djcelery',
    'sorl.thumbnail',
    'templatetag_handlebars',
    'bootstrap',
    'tastypie',
    # helpers
    'django_extensions',
    'haystack',
    'annoying',
    'south',
)

PROJECT_APPS = (
    # Default - Install the shopify app
    'cartvine.apps.default',
    # Product email
    'cartvine.apps.mail',
    # Application Settings - Allow user to modify the settings
    'cartvine.apps.app_settings',
    # Shop
    'cartvine.apps.shop',
    # Customer - People who come to review after purchasing a product from the Shop
    'cartvine.apps.customer',
    # Product
    'cartvine.apps.product',
    # Plans
    'cartvine.apps.plan',
    # Webhook
    'cartvine.apps.webhook',
    # Widgets JS
    'cartvine.apps.widget',
    # API
    'cartvine.apps.api',
)

# Assemble them all together
INSTALLED_APPS = BASE_APPS + HELPER_APPS + PROJECT_APPS

LOGIN_URL = '/login/'
CUSTOMER_LOGIN_URL_NAME = '/customer/login/'

# Django Debug Toolbar
if DEBUG:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)
    INTERNAL_IPS = ('127.0.0.1', '172.16.37.128')
    DEBUG_TOOLBAR_CONFIG = {
      'INTERCEPT_REDIRECTS': False
    }
    # Postback for the dev webhook interface
    # Define in your local_settings.py
    # WEBHOOK_POSTBACK_HOST = 'http://178.200.223.240:8000'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(SITE_ROOT, '../data/search/product_index'),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
        'SILENTLY_FAIL': True,
    },
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(module)s - %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'lumberjack': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(SITE_ROOT, 'log/cartvine.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'happy_log': {
            'handlers': ['lumberjack'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Django Celery
CELERY_RESULT_BACKEND = "amqp"
BROKER_URL = "amqp://guest@localhost:5672//"
CELERY_TASK_RESULT_EXPIRES = 30

# Email Templates
TEMPLATED_EMAIL_TEMPLATE_DIR = 'templated_email/'
TEMPLATED_EMAIL_FILE_EXTENSION = 'email'

TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django.TemplateBackend'
# You can also use shortcut version
TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django'
# For the django back-end specifically
TEMPLATED_EMAIL_DJANGO_SUBJECTS = {
    'welcome':'Thanks and are you happy with your purchased product?',
}

FACEBOOK_APP_ID = '209234305864956'
FACEBOOK_SECRET_KEY = 'd0875d1310c3708181b5b9d2092593d8'

# Custom test runner for this project
TEST_RUNNER = 'cartvine.test_runner.CartvineAppTestRunner'

# Remote images are downloaded and stored in this folder relative to the MEDIA_ROOT
REMOTE_IMAGE_STORAGE_PATH = 'remote'

# Handlebars render style
USE_EMBER_STYLE_ATTRS = False


try:
    from shopify_settings import *
except ImportError:
    pass

try:
    from local_settings import *
except ImportError:
    pass
