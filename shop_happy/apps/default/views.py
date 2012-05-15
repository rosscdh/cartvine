from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView, RedirectView


from forms import ShopifyInstallForm
import shopify


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
    url = '/'


class FinalizeInstallationView(RedirectView):
    def get(self, request, *args, **kwargs):
        shop_url = request.REQUEST.get('shop')
        try:
            shopify_session = shopify.Session(shop_url, request.REQUEST)
        except shopify.ValidationException:
            messages.error(request, _('Could not log in to Shopify store.'))
            return redirect(reverse('default:login'))

        request.session['shopify'] = shopify_session
        messages.info(request, _('Sucessfully logged into your shopify store.'))

        response = redirect(_return_address(request))
        request.session.pop('return_to', None)

        return response
