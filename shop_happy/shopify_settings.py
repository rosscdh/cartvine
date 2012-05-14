import os
# Replace the API Key and Shared Secret with the one given for your
# App by Shopify.
#
# To create an application, or find the API Key and Secret, visit:
# - for private Apps:
#     https://${YOUR_SHOP_NAME}.myshopify.com/admin/api
# - for partner Apps:
#     https://www.shopify.com/services/partners/api_clients
#
# You can ignore this file in git using the following command:
#   git update-index --assume-unchanged shopify_settings.py
# SHOPIFY_API_KEY = os.getenv('SHOPIFY_API_KEY')
# SHOPIFY_API_SECRET = os.getenv('SHOPIFY_API_SECRET')

SHOPIFY_API_KEY = '587b6f824f4a5d1d850a720f90f4a3b5'
SHOPIFY_API_SECRET = 'd9f012af184b44c31f1dff094feed795'

# oauth2 scope decleration
SHOPIFY_ACCESS_SCOPE = ['write_content', 'write_themes', 'write_products', 'write_customers', 'write_orders', 'write_script_tags', 'write_shipping']
