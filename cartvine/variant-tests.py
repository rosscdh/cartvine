import shopify
s = Shop.objects.get(pk=1)
s.activate_shopify_session()
p=shopify.Product.find(92048506)

v = shopify.Variant(dict(sku='test1', product_id=92048506, price="20.00"))

v = shopify.Variant(dict(sku='test1', product_id=92048506, price="20.00", option1="Second"))
