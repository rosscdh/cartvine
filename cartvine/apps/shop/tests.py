"""
Test the Shop object and views
"""
from django.contrib.auth.models import User
from django.test.client import Client
from django.test import TestCase
from django.core.urlresolvers import reverse

from models import Shop



class ShopTest(TestCase):

    def setUp(self):
        User.objects.create_user('usera', 'usera@test.com', 'test')
        self.user_a = User.objects.get(username='usera')

        Shop.objects.create(name='shop a',provider_id=1234567, shopify_access_token=1234567,slug='shop-a',url='shop-a.myshopify.com')
        self.shop = Shop.objects.get(slug='shop-a')
        self.shop.users.add(self.user_a)

