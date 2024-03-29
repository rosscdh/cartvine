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
from models import Product


login_required_urls = [
    reverse('product:index'), 
    reverse('product:info', kwargs={'slug': 'test-product-1'}), 
    ]


class ProductTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Setup fixtures
        # create user a
        User.objects.create_user('usera', 'usera@test.com', 'test')
        self.user_a = User.objects.get(username='usera')

        Shop.objects.create(name='shop a',provider_id=1234567, provider_access_token=1234567,slug='shop-a',url='shop-a.myshopify.com')
        shop_a = Shop.objects.get(slug='shop-a')
        shop_a.users.add(self.user_a)
        # create user products and associate with user1
        self.user_a_products = self.__create_products_for_shop(shop_a)

        # create user b
        User.objects.create_user('userb', 'userb@test.com', 'test')
        self.user_b = User.objects.get(username='userb')
        Shop.objects.create(name='shop b',provider_id=2345678, provider_access_token=2345678,slug='shop-b',url='shop-b.myshopify.com')
        shop_b = Shop.objects.get(slug='shop-b')
        shop_b.users.add(self.user_b)
        # create second user products and assocaited with user2
        self.user_b_products = self.__create_products_for_shop(shop_b)

    def __create_products_for_shop(self, shop, num_products=5):
        """ Utility method to Create X number of products for the provided shop object """
        product_list = []
        for i in range(1,num_products+1):
            provider_id = shop.pk + (i*1000)
            name = 'Product %d for Shop %s' %(i,shop.name,)
            data = {
                'body_html': '<p>Test Product HTML</p>',
                'product_type': 'Test Product',
            }
            p = Product.objects.create(shop=shop, provider_id=provider_id, name=name, slug=provider_id, data=data)
            product_list.append(p)
        return product_list
        
    def test_anonymous_cannot_access_logged_in_urls(self):
        """ test primary logged in urls cannot be acessed unless logged in """
        for u in login_required_urls:
            response = self.client.get(u, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['current_shop'], None)
            self.assertTrue(isinstance(response.context['form'], ShopifyInstallForm))

    def test_product_list_view(self):
        """ test that when logged in the user can see their list of products (only their products) """
        # log user 1 in
        self.client.login(username='usera', password='test')

        # test user1 can see products
        # test user1 can see only their products
        response = self.client.get(reverse('product:index'))

        self.assertTrue(isinstance(response.context['object_list'], QuerySet))
        self.assertEqual(response.context['object_list'].count(), 5)
        # ensure that none of user Bs products are in this list
        self.assertTrue(self.user_b_products not in response.context['object_list'])

    def test_product_detail_view(self):
        self.client.login(username='usera', password='test')
        response = self.client.get(reverse('product:info', kwargs={'slug': self.user_a_products[0].slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], self.user_a_products[0])
        

    def test_product_detail_view_access_by_non_owner(self):
        """ Log user B in and try to view userAs products """
        self.client.login(username='userb', password='test')

        response = self.client.get(reverse('product:info', kwargs={'slug': self.user_a_products[0].slug}))
        self.assertEqual(response.status_code, 404)


class ProductTemplateTagsTest(TestCase):
    """ Test the Product templatetags """
    def setUp(self):
        pass

    def test_tag_image_reseize(self):
        """ Test the image_resize template tag 
        shopify makes a series of image sizes available via the api
        cartvine.apps.product.templatetags.product_tags.SHOP_IMAGE_SIZE
        image_resize returns
        http://static.shopify.com/s/files/1/0157/5666/products/ant_water_%s.jpg?107
        http://static.shopify.com/s/files/1/0157/5666/products/ant_water_[pico,small...].jpg?107
        ...
        """
        from cartvine.apps.product.templatetags.product_tags import SHOP_IMAGE_SIZE
        image = 'http://static.shopify.com/s/files/1/0157/5666/products/ant_water%s.jpg?107'
        # Default resie
        src = image_resize(image%('',))
        self.assertEqual(src, 'http://static.shopify.com/s/files/1/0157/5666/products/ant_water_compact.jpg?107')
        # remove the %s palceholder
        image = image%('',)
        for size in SHOP_IMAGE_SIZE:
            src = image_resize(image, size)
            self.assertEqual(src, 'http://static.shopify.com/s/files/1/0157/5666/products/ant_water%s.jpg?107'%('_'+size,))

