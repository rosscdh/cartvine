"""
Test the default app views
"""
from django.test.client import Client
from django.test import TestCase

from django.core.urlresolvers import reverse

from shop_happy.apps.default.forms import ShopifyInstallForm

login_required_urls = [
		reverse('my_app:settings'), 
		reverse('my_app:design'), 
		]

class AppSettingsTest(TestCase):
	def setUp(self):
		self.client = Client()

	def test_anonymous_cannot_access_logged_in_urls(self):
		""" test primary logged in urls cannot be acessed unless logged in """
		for u in login_required_urls:
			response = self.client.get(u, follow=True)
			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.context['current_shop'], None)
			self.assertTrue(isinstance(response.context['form'], ShopifyInstallForm))

