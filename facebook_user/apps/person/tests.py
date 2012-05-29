"""
Test the default app views
"""
from django.contrib.auth.models import User
from django.test.client import Client
from django.test import TestCase
from django.db.models.query import QuerySet
from django.core.urlresolvers import reverse

from cartvine.apps.default.forms import ShopifyInstallForm
from cartvine.apps.shop.models import Shop
from cartvine.apps.product.templatetags.product_tags import image_resize

from models import Person

from django.utils import simplejson as json

app_urls = {
    'validate': reverse('person:validate', kwargs={'application_type': 'facebook',}),
    }


class PersonTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Setup fixtures
        self.valid_post_body = {
            'uid': '',
            'access_token': '',
            'username': '',
            'email': '',
            'first_name': '',
            'last_name': '',
        }

    def test_validation_view_get_invalid(self):
        """ test that invalid get options to the person validation url errors out """
        # invalid application_type
        url = reverse('person:validate', kwargs={'application_type': 'monkey',})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
        # get is invalid only post valid
        response = self.client.get(app_urls['validate'])
        self.assertEqual(response.status_code, 405)

    def test_validation_view_post_invalid(self):
        """ test that invalid post options to the person validation url errors out """
        # invalid application_type
        url = reverse('person:validate', kwargs={'application_type': 'monkey',})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

        response = self.client.post(app_urls['validate'], json.dumps(self.valid_post_body), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_validation_view_post_valid(self):
        self.valid_post_body['uid'] = '1234567890'
        self.valid_post_body['access_token'] = 'ABCDEFGH'
        self.valid_post_body['username'] = 'tester'
        self.valid_post_body['email'] = 'test@rulenoone.com'
        self.valid_post_body['first_name'] = 'Test'
        self.valid_post_body['last_name'] = 'Me'
        
        response = self.client.post(app_urls['validate'], json.dumps(self.valid_post_body), content_type='application/json')
        self.assertEqual(response.status_code, 404)

