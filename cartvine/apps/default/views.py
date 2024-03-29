from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView, RedirectView


import shopify

from cartvine.apps.shop.models import Shop
from cartvine.apps.webhook.models import Webhook

from forms import ShopifyInstallForm

from cartvine.utils import get_webhook_postback_url
from cartvine.apps.product.tasks import sync_products
from cartvine.apps.customer.tasks import sync_customers
from cartvine.apps.webhook.tasks import sync_webhook
from cartvine.apps.widget.tasks import sync_assets


import logging
logger = logging.getLogger('happy_log')


def _return_address(request):
    url_append = None
    if request.GET.get('next', None) is not None:
        if request.GET.get('id', None) is not None:
            url_append = '?id=%s' %(request.GET.get('id'),)
        return request.GET.get('next') + url_append
    else:
        return request.session.get('return_to') or reverse('default:index')


class DefaultView(TemplateView):
    template_name = 'default/default.html'

    def get(self, request, *args, **kwargs):
        shop = request.REQUEST.get('shop')

        if shop:
            redirect_uri = request.build_absolute_uri(reverse('default:finalize'))
            if request.GET.get('next', None) is not None:
                url_append = '?next=%s' %(request.GET.get('next'))
                if request.GET.get('id', None) is not None:
                    url_append = '%s&id=%s' %(url_append, request.GET.get('id'))
                redirect_uri += url_append

            permission_url = shopify.Session.create_permission_url(shop.strip(), scope=settings.SHOPIFY_ACCESS_SCOPE, redirect_uri=redirect_uri)
            return redirect(permission_url)

        form = ShopifyInstallForm()

        return self.render_to_response({
            'form': form,
        })


class LogoutView(RedirectView):
    """ Log the user out """
    def get(self, request, *args, **kwargs):
        # Clear shopify Session
        # if hasattr(request, 'session') and 'shopify' in request.session:
        #     shopify.ShopifyResource.clear_session()
        #     request.session.pop('shopify', None)
        logout(request)
        messages.info(request, _('Successfully logged out.'))

        return redirect(reverse('default:index'))


# LoginView - Effectively the same thing.. our login is dependent on the shopify api
class FinalizeInstallationView(RedirectView):
    """
    Class finalizes the login process and will create the shop as well as user
    if they do not exist. Has been written to cater to multiple users associated
    with one shop
    """

    def get(self, request, *args, **kwargs):
        shop_url = request.REQUEST.get('shop', None)

        if shop_url:
            try:
                shopify_session = shopify.Session(shop_url, request.REQUEST)
            except shopify.ValidationException:
                messages.error(request, _('Could not log in to Shopify store.'))
                logger.error('FinalizeIntallationView: Could not login %s' % (shopify.ValidationException,))
                return redirect(reverse('default:login'))
            
            # Create/Get Shopify Shop
            shop = Shop.objects.get_or_create_shop(shopify_session)
            # Create/Get Shopify User
            user = Shop.objects.get_or_create_owner(shop)

            # Get the user logged in if possible
            authenticate(user=user, access_token=shopify_session.token)
            login(request, user)

            webhook_callback_address = get_webhook_postback_url(request, reverse('webhook:invite_review_create'))

            try:
                # Create/Get Shopify Webhook
                sync_webhook.delay(webhook_callback_address, shop)
                sync_assets.delay(shop)
                # Call Product Sync Task here
                sync_products.delay(shop)
                sync_customers.delay(shop)
            except:
                # Try the same calls without the celery async .delay()
                sync_webhook(webhook_callback_address, shop)
                sync_assets(shop)
                sync_products(shop)
                sync_customers(shop)

            # Setup the shopify session and show message
            request.session['shopify'] = shopify_session
            messages.info(request, _('You have successfully, logged into Cartvine'))

        response = redirect(_return_address(request))
        request.session.pop('return_to', None)
        logger.info('Logged in as %s token:%s' % (user, shopify_session.token,))

        return response
