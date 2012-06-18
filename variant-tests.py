import shopify
s = Shop.objects.get(pk=1)
s.activate_shopify_session()

v = shopify.Variant.create(dict(sku='test/sku-1', title='My Test Unique SKU', price='25.00', compare_at_price='15.00', available=True, inventory_management='shopify', inventory_quantity=1, weight=0, option1='a', option2='b', option3='c', options='', requires_shipping=False, taxable=True))
v2 = shopify.Variant.create(dict(sku='test/sku-2', title='My Test Unique SKU 2', price='25.00', compare_at_price='15.00', available=True, inventory_management='shopify', inventory_quantity=1, weight=0, option1='a', option2='b', option3='c', options='', requires_shipping=False, taxable=True))

p=shopify.Product.find(92048506)
v = shopify.Variant.create(dict(product_id=p.id, sku='test/sku-1', title='My Test Unique SKU', price='25.00', compare_at_price='15.00', option1='a', option2='b', option3='c', options='', requires_shipping=False, taxable=True))