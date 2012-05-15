from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView, RedirectView

import shopify

from django.contrib.auth.models import User
from shop_happy.apps.shop.models import Shop

from forms import ShopifyInstallForm


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


class LoginView(TemplateView):
    pass


class LogoutView(RedirectView):

    def get(self, request, *args, **kwargs):
        # Clear shopify Session
        shopify.ShopifyResource.clear_session()
        request.session.pop('shopify', None)
        messages.info(request, _('Successfully logged out.'))

        return redirect(reverse('default:index'))


class FinalizeInstallationView(RedirectView):

    def get_or_create_shop(self, shopify_session):
        shopify.ShopifyResource.activate_session(shopify_session)

        current_shop = shopify.Shop.current()

        domain_parts = current_shop.__dict__['attributes']['domain'].split('.')

        shop, is_new = Shop.objects.get_or_create(shopify_id=current_shop.id, slug=domain_parts[0], url=shopify_session.site, name=current_shop.name)
        shop.data = current_shop.__dict__['attributes']
        shop.save()

        return shop

    def get_or_create_user(self, shop):
        assert False
        user = User.objects.get_or_create()
        return None

    def get(self, request, *args, **kwargs):
        shop_url = request.REQUEST.get('shop', None)
        if shop_url:
            try:
                shopify_session = shopify.Session(shop_url, request.REQUEST)
            except shopify.ValidationException:
                messages.error(request, _('Could not log in to Shopify store.'))
                return redirect(reverse('default:login'))

            shop = self.get_or_create_shop(shopify_session)
            user = self.get_or_create_user(shop)

            request.session['shopify'] = shopify_session

            messages.info(request, _('Sucessfully logged into your shopify store.'))

        response = redirect(_return_address(request))
        request.session.pop('return_to', None)

        return response
