"""
Test the Mail app for CartVine
"""

from django.test import TestCase

from cartvine.apps.shop.models import Shop
from cartvine.apps.customer.models import Customer
from cartvine.apps.mail.models import CartvineEmail
from cartvine.apps.webhook.models import OrderCreatePostback

import datetime
from dateutil import parser


class MailTest(TestCase):

	def test_get_email_post_date(self):
		""" test the @static_method on the CartvineEmail model that 
		returns a date 2 weeks in the future
		"""
		date_from = datetime.datetime(2012,05,21,0,0)
		date_expected = date_from + datetime.timedelta(weeks=2)

		dateof = CartvineEmail.get_email_post_date(date_from.strftime('%Y-%m-%d'))
		self.assertEqual(date_expected, dateof)

	def test_create_email_from_callback(self):
		""" Test the email object is created from a valid callback """
		date_from = datetime.datetime.today()
		date_expected = date_from + datetime.timedelta(weeks=2)

		test_shop = Shop.objects.create(name='Test Shop 1', slug='test-shop-1', url='http://test-shop-1.myshopify.com', provider_id=1234567)

		data = {
			'customer': {
				'first_name': 'Jack',
				'last_name': 'Johnson',
				'email': 'jack@test.com',
			},
			'line_items': [],
		}

		order = OrderCreatePostback.objects.create(shop=test_shop, shop_url=test_shop.url, content_type='json', recieved_from='localhost', recieved_from_ip='127.0.0.1', data=data)

		email = CartvineEmail.objects.create_email_from_callback(order)

		self.assertEqual(email.shop, test_shop)
		self.assertTrue(isinstance(email.customer, Customer))
		self.assertEqual(email.email_to, data['customer']['email'])
		self.assertEqual(email.email_to, email.customer.email)
		self.assertEqual(email.post_date, date_expected.date())
		self.assertEqual(email.sent_date, None)