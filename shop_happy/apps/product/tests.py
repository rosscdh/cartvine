"""
Test the default app views
"""
from django.contrib.auth.models import User
from django.test.client import Client
from django.test import TestCase

from django.core.urlresolvers import reverse

from shop_happy.apps.default.forms import ShopifyInstallForm
from shop_happy.apps.shop.models import Shop
from models import Product

login_required_urls = [
		reverse('product:index'), 
		reverse('product:info', kwargs={'slug': 'test-product-1'}), 
		]


class ProductTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_anonymous_cannot_access_logged_in_urls(self):
        """ test primary logged in urls cannot be acessed unless logged in """
        for u in login_required_urls:
            response = self.client.get(u, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['current_shop'], None)
            self.assertTrue(isinstance(response.context['form'], ShopifyInstallForm))

    def test_product_list_view(self):
        """ test that when logged in the user can see their list of products (only their products) """
        # create user
        shop_a = Shop.objects.create(name='shop a',shopify_id=1234567, shopify_access_token=1234567,slug='shop-a',url='shop-a.myshopify.com')
        user_a = User.objects.create(username='usera', email='usera@test.com')
        shop_a.users.add(user_a)
        # create user products and associate with user1
        self.create_products_for_user(shop_a)
        # create second user
        shop_b = Shop.objects.create(name='shop b',shopify_id=2345678, shopify_access_token=2345678,slug='shop-b',url='shop-b.myshopify.com')
        user_b = User.objects.create(username='userb', email='userb@test.com')
        shop_b.users.add(user_b)
        # create second user products and assocaited with user2
        self.create_products_for_user(shop_b)
        # log user 1 in
        # test user1 can see products
        # test user1 can see only their products
        response = self.client.get(reverse('product:index'))
        print response.status_code

    def create_products_for_user(self, shop, num_products=5):
        """ Create X number of products for the provided shop object """
        product_list = []
        for i in range(1,num_products):
            shopify_id = (i*1000)
            name = 'Product %d for Shop %s' %(i,shop.name,)
            data = {
                'body_html': '<p>Test Product HTML</p>',
                'product_type': 'Test Product',
            }
            p = Product.objects.create(shop=shop, shopify_id=shopify_id, name=name, slug=shopify_id, data=data)
            product_list.append(p)
        return product_list
        