from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured

import shopify


class WebhookManager(models.Manager):
    """ Manager for Webhook objects 
    Provides accessor methods that wrap around the shopify api
    """
    def create_webhook_if_not_exists(self, shopify_webhook, shop):
        # Create the local Webhook object
        return self.get_or_create(shop=shop, shopify_id=webhook.id, topic=webhook.topic, address=webhook.address, format=webhook.format)

