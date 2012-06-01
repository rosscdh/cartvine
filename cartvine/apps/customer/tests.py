"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Customer


class CustomerTest(TestCase):
    def setUp(self):
		self.customer_data = {
			'customer': {
				'first_name': 'Jack',
				'last_name': 'Johnson',
				'email': 'jack@test.com',
			},
			'line_items': [],
		}

    def test_get_customer_full_name(self):
        """
        Test that we get the full name of a generated customer
        """
        customer = Customer.objects.create(provider_id=1234567,first_name=self.customer_data['customer']['first_name'],last_name=self.customer_data['customer']['last_name'],email=self.customer_data['customer']['email'],data=self.customer_data)
        test_name = u'%s %s' %(self.customer_data['customer']['first_name'],self.customer_data['customer']['last_name'],)
        self.assertEqual(customer.get_full_name, test_name)
