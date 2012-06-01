"""
Test the default app views
"""
from django.contrib.auth.models import User
from django.test.client import Client
from django.test import TestCase
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

from cartvine.apps.shop.models import Shop
from cartvine.apps.widget.models import Widget, WidgetShop


login_required_urls = [
    reverse('widget:edit', kwargs={'slug': 'test-widget'}),
    reverse('widget:my'),
    reverse('widget:info', kwargs={'slug': 'test-widget'}),
    reverse('widget:buy', kwargs={'slug': 'test-widget'}),
    reverse('widget:default'),
]
open_urls = [
    reverse('widget:widget_loader'),
    reverse('widget:for_shop', kwargs={'slug': 'test-shop'}),
    reverse('widget:script', kwargs={'shop_slug': 'test-shop', 'slug': 'test-widget'}),
]


class CartVineWidgetTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('usera', 'usera@test.com', 'test')
        self.test_shop, is_new = Shop.objects.get_or_create(name='Test Shop', provider_id=1, provider_access_token=12345, slug='test-shop', url='')
        self.test_shop.users.add(self.user)
        self.test_shop.save()
        self.test_widget, is_new = Widget.objects.get_or_create(name='Test JS Widget', widget_type=Widget.WIDGET_TYPE.text_javascript, slug='test-widget')
        self.widget_config = WidgetShop.objects.get_or_create(widget=self.test_widget, shop=self.test_shop)
        self.test_widget.save()

    def test_anonymous_cannot_access_logged_in_urls(self):
        """ test primary logged in urls cannot be acessed unless logged in """
        for u in login_required_urls:
            response = self.client.get(u)
            self.assertTrue(response.status_code in [302,404])

    def test_authenticated_and_anonymous_can_access_urls(self):
        """ Test urls that are totally open """
        # user = self.user
        # authenticate(user=user, username='usera', password='test')
        # login(self.client.request, user)
        for u in open_urls:
            response = self.client.get(u, follow=True)
            print u
            self.assertEqual(response.status_code, 200)


