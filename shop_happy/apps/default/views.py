from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView, RedirectView


import shopify

from shop_happy.apps.shop.models import Shop
from shop_happy.apps.webhook.models import Webhook

from forms import ShopifyInstallForm

from shop_happy.utils import get_webhook_postback_url
from shop_happy.apps.product.tasks import sync_products
from shop_happy.apps.customer.tasks import sync_customers
from shop_happy.apps.webhook.tasks import sync_webhook



def _return_address(request):
    return request.session.get('return_to') or reverse('default:index')


class DefaultView(TemplateView):
    template_name = 'default/default.html'

    def get(self, request, *args, **kwargs):
        shop = request.REQUEST.get('shop')

        if shop:
            redirect_uri = request.build_absolute_uri(reverse('default:finalize'))
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
                return redirect(reverse('default:login'))
            
            # Create/Get Shopify Shop
            shop = Shop.objects.get_or_create_shop(shopify_session)
            # Create/Get Shopify User
            user = Shop.objects.get_or_create_owner(shop)

            # Get the user logged in if possible
            authenticate(user=user, access_token=shopify_session.token)
            login(request, user)

            webhook_callback_address = get_webhook_postback_url(request, reverse('webhook:invite_review_create'))

            # try:
            #     # Create/Get Shopify Webhook
            #     sync_webhook.delay(webhook_callback_address, shop, shopify_session)
            #     # Call Product Sync Task here
            #     sync_products.delay(shopify_session, shop)
            #     sync_customers.delay(shopify_session, shop)
            # except:
            # Try the same calls without the celery async .delay()
            sync_webhook(webhook_callback_address, shop, shopify_session)
            sync_products(shopify_session, shop)
            sync_customers(shopify_session, shop)

            # Setup the shopify session and show message
            request.session['shopify'] = shopify_session
            messages.info(request, _('Sucessfully logged into your shopify store.'))

        response = redirect(_return_address(request))
        request.session.pop('return_to', None)

        return response
