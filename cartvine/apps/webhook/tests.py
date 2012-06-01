"""
Test teh shopify webhoook which is created on owner signup and login
and then populated on every puchase order/create webhook on the shopify side
"""
from django.contrib.auth.models import User
from django.test.client import Client
from django.test import TestCase

from django.core.urlresolvers import reverse
from django.test import TestCase

from cartvine.apps.shop.models import Shop
from models import OrderCreatePostback

from django.utils import simplejson as json


class WebhookTest(TestCase):
    def setUp(self):
        self.webhook_url = reverse('webhook:invite_review_create')

        self.client = Client()
        User.objects.create_user('usera', 'usera@test.com', 'test')
        self.user_a = User.objects.get(username='usera')

        shop_domain = 'shop-a.myshopify.com'
        Shop.objects.create(name='shop a',provider_id=1234567, provider_access_token=1234567,slug='shop-a',url='http://%s'%(shop_domain,))
        self.shop = Shop.objects.get(slug='shop-a')
        self.shop.users.add(self.user_a)

        self.request_domain = shop_domain
        self.request_hash = 'Hash12345'
        self.request_data = '{"buyer_accepts_marketing":true,"cancel_reason":"customer","cancelled_at":"2012-05-17T06:57:52-04:00","cart_token":null,"closed_at":null,"created_at":"2012-05-17T06:57:52-04:00","currency":"USD","email":"jon@doe.ca","financial_status":"voided","fulfillment_status":"pending","gateway":"bogus","id":123456,"landing_site":null,"name":"#9999","note":null,"number":234,"referring_site":null,"subtotal_price":"229.94","taxes_included":false,"token":null,"total_discounts":"0.00","total_line_items_price":"229.94","total_price":"239.94","total_tax":"0.00","total_weight":0,"updated_at":"2012-05-17T06:57:52-04:00","browser_ip":null,"landing_site_ref":null,"order_number":1234,"discount_codes":[],"note_attributes":[],"processing_method":null,"line_items":[{"fulfillment_service":"manual","fulfillment_status":null,"grams":5000,"price":"199.99","product_id":null,"quantity":1,"requires_shipping":true,"sku":"SKU2006-001","title":"Sledgehammer","variant_id":null,"variant_title":null,"vendor":null,"name":"Sledgehammer","variant_inventory_management":null},{"fulfillment_service":"manual","fulfillment_status":null,"grams":500,"price":"29.95","product_id":null,"quantity":1,"requires_shipping":true,"sku":"SKU2006-020","title":"Wire Cutter","variant_id":null,"variant_title":null,"vendor":null,"name":"Wire Cutter","variant_inventory_management":null}],"shipping_lines":[{"code":null,"price":"10.00","source":"shopify","title":"Generic Shipping"}],"tax_lines":[],"billing_address":{"address1":"123 Billing Street","address2":null,"city":"Billtown","company":"My Company","country":"United States","first_name":"Bob","last_name":"Biller","latitude":null,"longitude":null,"phone":"555-555-BILL","province":"Kentucky","zip":"K2P0B0","name":"Bob Biller","country_code":"US","province_code":"KY"},"shipping_address":{"address1":"123 Shipping Street","address2":null,"city":"Shippington","company":"Shipping Company","country":"United States","first_name":"Steve","last_name":"Shipper","latitude":null,"longitude":null,"phone":"555-555-SHIP","province":"Kentucky","zip":"K2P0S0","name":"Steve Shipper","country_code":"US","province_code":"KY"},"fulfillments":[],"customer":{"accepts_marketing":null,"created_at":null,"email":"john@test.com","first_name":"John","last_name":"Smith","last_order_id":null,"note":null,"orders_count":0,"state":"disabled","total_spent":"0.00","updated_at":null,"tags":"","last_order_name":null}}'

    def test_invalid_postback_meta(self):
        """
        On reciept of the postback, shopify is required to specify the
        HTTP_X_SHOPIFY_SHOP_DOMAIN as well as HTTP_X_SHOPIFY_HMAC_SHA256 
        used in verification of request
        """
        response = self.client.post(self.webhook_url, self.request_data, 'text/json') #@TODO find out how to set post_raw_data in django Client
        # shoud be 404 as the HTTP_X_SHOPIFY_SHOP_DOMAIN was not posted
        self.assertEqual(response.status_code, 404)


    def test_valid_postback_meta(self):
        """
        On reciept of the postback, shopify is required to specify the
        HTTP_X_SHOPIFY_SHOP_DOMAIN as well as HTTP_X_SHOPIFY_HMAC_SHA256 
        used in verification of request
        """
        # should not 404 as we specify the HTTP_X_SHOPIFY_SHOP_DOMAIN
        response = self.client.post(self.webhook_url, self.request_data, 'text/json', HTTP_X_SHOPIFY_HMAC_SHA256=self.request_hash, HTTP_X_SHOPIFY_SHOP_DOMAIN=self.request_domain) #@TODO find out how to set post_raw_data in django Client
        self.assertEqual(response.status_code, 200)

        order = OrderCreatePostback.objects.order_by('-date_recieved').get( shop_url='http://%s'%(self.request_domain,) )

        self.assertEqual(order.shop, self.shop)
        self.assertEqual(order.shop_url, 'http://%s'%(self.request_domain,))
        self.assertEqual(response.context['response'], [order.pk])
