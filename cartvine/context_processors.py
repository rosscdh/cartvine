from django.contrib.sites.models import Site
import shopify

def current_shop(request):
    if not shopify.ShopifyResource.site:
        return {'current_shop': None}
    return {'current_shop': shopify.Shop.current()}


def cartvine_sites(request):
    site_list = Site.objects.all()
    try:
        return {
            'shopify_app_domain': site_list[0].domain,
            'shoppers_app_domain': site_list[1].domain,
        }
    except IndexError:
        return {
            'shopify_app_domain': 'define.your.sites',
            'shoppers_app_domain': 'define.your.sites',
        }

