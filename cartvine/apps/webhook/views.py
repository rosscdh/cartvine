from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic import FormView
from django.utils import simplejson as json

import shopify
import logging
logger = logging.getLogger('happy_log')

from cartvine.apps.mail.models import CartvineEmail
from cartvine.apps.shop.models import Shop

from models import OrderCreatePostback

# curl -H "HTTP_X_SHOPIFY_SHOP_DOMAIN: price-turcotte-and-gleichner1525.myshopify.com" '{"buyer_accepts_marketing":true,"cancel_reason":"customer","cancelled_at":"2012-05-17T06:57:52-04:00","cart_token":null,"closed_at":null,"created_at":"2012-05-17T06:57:52-04:00","currency":"USD","email":"jon@doe.ca","financial_status":"voided","fulfillment_status":"pending","gateway":"bogus","id":123456,"landing_site":null,"name":"#9999","note":null,"number":234,"referring_site":null,"subtotal_price":"229.94","taxes_included":false,"token":null,"total_discounts":"0.00","total_line_items_price":"229.94","total_price":"239.94","total_tax":"0.00","total_weight":0,"updated_at":"2012-05-17T06:57:52-04:00","browser_ip":null,"landing_site_ref":null,"order_number":1234,"discount_codes":[],"note_attributes":[],"processing_method":null,"line_items":[{"fulfillment_service":"manual","fulfillment_status":null,"grams":5000,"price":"199.99","product_id":null,"quantity":1,"requires_shipping":true,"sku":"SKU2006-001","title":"Sledgehammer","variant_id":null,"variant_title":null,"vendor":null,"name":"Sledgehammer","variant_inventory_management":null},{"fulfillment_service":"manual","fulfillment_status":null,"grams":500,"price":"29.95","product_id":null,"quantity":1,"requires_shipping":true,"sku":"SKU2006-020","title":"Wire Cutter","variant_id":null,"variant_title":null,"vendor":null,"name":"Wire Cutter","variant_inventory_management":null}],"shipping_lines":[{"code":null,"price":"10.00","source":"shopify","title":"Generic Shipping"}],"tax_lines":[],"billing_address":{"address1":"123 Billing Street","address2":null,"city":"Billtown","company":"My Company","country":"United States","first_name":"Bob","last_name":"Biller","latitude":null,"longitude":null,"phone":"555-555-BILL","province":"Kentucky","zip":"K2P0B0","name":"Bob Biller","country_code":"US","province_code":"KY"},"shipping_address":{"address1":"123 Shipping Street","address2":null,"city":"Shippington","company":"Shipping Company","country":"United States","first_name":"Steve","last_name":"Shipper","latitude":null,"longitude":null,"phone":"555-555-SHIP","province":"Kentucky","zip":"K2P0S0","name":"Steve Shipper","country_code":"US","province_code":"KY"},"fulfillments":[],"customer":{"accepts_marketing":null,"created_at":null,"email":"john@test.com","first_name":"John","last_name":"Smith","last_order_id":null,"note":null,"orders_count":0,"state":"disabled","total_spent":"0.00","updated_at":null,"tags":"","last_order_name":null}}'

def CreateInvite(request):
    body = None
    if not request.META.get('HTTP_X_SHOPIFY_SHOP_DOMAIN', None):
        logger.error('Webhook Callback from shopify did not contain HTTP_X_SHOPIFY_SHOP_DOMAIN header %s' %(request.META,))
        raise Http404
    else:
        request_body = request.read()
        try:
            body = json.loads(request_body)
        except:
            logger.error('Webhook Callback from shopify could not parse response body as JSON')

        if not body:
            logger.error('Webhook Callback from shopify body is not valid %s'%(request_body,))
            raise Http404
        else:
            shop_domain = request.META.get('HTTP_X_SHOPIFY_SHOP_DOMAIN')
            # Token is not present if webhook is created via teh web interface
            webhook_verification_token = request.META.get('HTTP_X_SHOPIFY_HMAC_SHA256') #@TODO verify this token via: http://wiki.shopify.com/Verifying_Webhooks
            
            logger.info('Webhook Callback from shopify contains HTTP_X_SHOPIFY_SHOP_DOMAIN header %s (%s)' %(shop_domain,webhook_verification_token,) )

            shop = Shop.objects.get(url=u'http://%s' %(shop_domain,) )
            order = OrderCreatePostback.objects.create(data=body, shop=shop, shop_url=shop.url, content_type=request.META.get('CONTENT_TYPE'), recieved_from=request.META.get('REMOTE_HOST'), recieved_from_ip=request.META.get('REMOTE_ADDR'))
            logger.info('Webhook Callback from shopify body is valid. OrderCreatePostback was created')

            email = CartvineEmail.objects.create_email_from_callback(order)

	return render_to_response('webhook/response.html', {
		'response': [order.pk],
	})


class InviteReviewView(FormView):
	template_name='webhook/response.html'
