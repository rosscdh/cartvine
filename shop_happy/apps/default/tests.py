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
		reverse('product:index'), 
		reverse('product:info', kwargs={'slug': 'test-product'}), 
		]

class ShopHappyDefaultAppTest(TestCase):
	def setUp(self):
		self.client = Client()

	def test_login_screen_shows_by_default(self):
		"""
		The user should alwys be redirected to the login/signup screen
		"""
		test_urls = ['/', '/login/', '/monkey/test/page/']
		for u in test_urls:
			response = self.client.get('/')
			self.assertEqual(response.status_code, 200)

			self.assertEqual(response.context['current_shop'], None)
			self.assertTrue(isinstance(response.context['form'], ShopifyInstallForm))

	def test_redirect_with_shop_get_param(self, response=None):
		""" if ?shop=XXX is specified then we redirect to shopify with oauth request and scope """
		if not response:
			response = self.client.get('/?shop=reebok-beats-nike-anyday', follow=True)

		url, status_code = response.redirect_chain[0]

		self.assertEqual(url , 'https://reebok-beats-nike-anyday.myshopify.com/admin/oauth/authorize?scope=write_content%2Cwrite_themes%2Cwrite_products%2Cwrite_customers%2Cwrite_orders%2Cwrite_script_tags%2Cwrite_shipping%2Cread_content%2Cread_themes%2Cread_products%2Cread_customers%2Cread_orders%2Cread_script_tags%2Cread_shipping&redirect_uri=http%3A%2F%2Ftestserver%2Ffinalize%2F&client_id=587b6f824f4a5d1d850a720f90f4a3b5')
		self.assertEqual(status_code, 302)

	def test_login(self):
		response = self.client.get('/login/')
		self.assertEqual(response.status_code, 200)
		self.assertTrue(isinstance(response.context['form'], ShopifyInstallForm))

		response = self.client.get('/', {'shop': 'reebok-beats-nike-anyday'}, follow=True)
		# test using predefined method
		self.test_redirect_with_shop_get_param(response)

	def test_anonymous_cannot_access_logged_in_urls(self):
		""" test primary logged in urls cannot be acessed unless logged in """
		for u in login_required_urls:
			response = self.client.get(u, follow=True)
			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.context['current_shop'], None)
			self.assertTrue(isinstance(response.context['form'], ShopifyInstallForm))

