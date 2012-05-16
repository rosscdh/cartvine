from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured

import shopify


class WebhookManager(models.Manager):
    """ Manager for Webhook objects 
    Provides accessor methods that wrap around the shopify api
    """
    def create_webhook_if_not_exists(self, request, shop):
        """ Create the webhook on the remote app if it does not exist """
        webhook_callback_address = request.build_absolute_uri(reverse('webhook:invite_review_create'))
        webhook = shopify.Webhook.find(address=webhook_callback_address)

        if not webhook:
            # Create it
            new_webhook = shopify.Webhook()
            new_webhook.topic = 'orders/create'
            new_webhook.address = webhook_callback_address
            new_webhook.format = 'json'
            new_webhook.save()

            # Try to get the newly created webhook again
            webhook = shopify.Webhook.find(address=webhook_callback_address)
            if not webhook:
                # no luck is probably the host
                raise ImproperlyConfigured('Suspect that %s is not allowed by remote host for shop %s' %(webhook_callback_address,shop,))
            else:
                # Create the local Webhook object
                webhook = self.add(shop=shop, shopify_id=webhook.id, topic=webhook.topic, address=webhook.address, format=webhook.format)

        return webhook

