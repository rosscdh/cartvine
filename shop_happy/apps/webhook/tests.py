"""
Test teh shopify webhoook which is created on owner signup and login
and then populated on every puchase order/create webhook on the shopify side
"""
from django.test.client import Client
from django.test import TestCase

from django.core.urlresolvers import reverse
from django.test import TestCase


class WebhookTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.request_domain = 'price-turcotte-and-gleichner1525.myshopify.com'
        self.request_data = '{"buyer_accepts_marketing":true,"cancel_reason":"customer","cancelled_at":"2012-05-17T06:57:52-04:00","cart_token":null,"closed_at":null,"created_at":"2012-05-17T06:57:52-04:00","currency":"USD","email":"jon@doe.ca","financial_status":"voided","fulfillment_status":"pending","gateway":"bogus","id":123456,"landing_site":null,"name":"#9999","note":null,"number":234,"referring_site":null,"subtotal_price":"229.94","taxes_included":false,"token":null,"total_discounts":"0.00","total_line_items_price":"229.94","total_price":"239.94","total_tax":"0.00","total_weight":0,"updated_at":"2012-05-17T06:57:52-04:00","browser_ip":null,"landing_site_ref":null,"order_number":1234,"discount_codes":[],"note_attributes":[],"processing_method":null,"line_items":[{"fulfillment_service":"manual","fulfillment_status":null,"grams":5000,"price":"199.99","product_id":null,"quantity":1,"requires_shipping":true,"sku":"SKU2006-001","title":"Sledgehammer","variant_id":null,"variant_title":null,"vendor":null,"name":"Sledgehammer","variant_inventory_management":null},{"fulfillment_service":"manual","fulfillment_status":null,"grams":500,"price":"29.95","product_id":null,"quantity":1,"requires_shipping":true,"sku":"SKU2006-020","title":"Wire Cutter","variant_id":null,"variant_title":null,"vendor":null,"name":"Wire Cutter","variant_inventory_management":null}],"shipping_lines":[{"code":null,"price":"10.00","source":"shopify","title":"Generic Shipping"}],"tax_lines":[],"billing_address":{"address1":"123 Billing Street","address2":null,"city":"Billtown","company":"My Company","country":"United States","first_name":"Bob","last_name":"Biller","latitude":null,"longitude":null,"phone":"555-555-BILL","province":"Kentucky","zip":"K2P0B0","name":"Bob Biller","country_code":"US","province_code":"KY"},"shipping_address":{"address1":"123 Shipping Street","address2":null,"city":"Shippington","company":"Shipping Company","country":"United States","first_name":"Steve","last_name":"Shipper","latitude":null,"longitude":null,"phone":"555-555-SHIP","province":"Kentucky","zip":"K2P0S0","name":"Steve Shipper","country_code":"US","province_code":"KY"},"fulfillments":[],"customer":{"accepts_marketing":null,"created_at":null,"email":"john@test.com","first_name":"John","last_name":"Smith","last_order_id":null,"note":null,"orders_count":0,"state":"disabled","total_spent":"0.00","updated_at":null,"tags":"","last_order_name":null}}'

    def test_postback_required_meta(self):
        """
        On reciept of the postback, shopify is required to specify the
        HTTP_X_SHOPIFY_SHOP_DOMAIN as well as HTTP_X_SHOPIFY_HMAC_SHA256 
        used in verification of request
        """
        url = reverse('webhook:invite_review_create')
        response = self.client.post(url, {'body': self.request_data}) #@TODO find out how to set post_raw_data in django Client
        # shoud be 404 as the HTTP_X_SHOPIFY_SHOP_DOMAIN was not posted
        self.assertEqual(response.status_code, 404)

