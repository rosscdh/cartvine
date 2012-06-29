from cartvine.apps.product.models import Product, get_property_dict

def add_slug():
    for p in Product.objects.all():
      print 'Product: %s' % (p.name, )
      for i,o in enumerate(p.all_properties()):
        if 'slug' not in o.keys():
          prop = get_property_dict(option_id=o['option_id'], name=o['name'], value=o['value'])
          print '%s BECOMES %s' % (p.data['all_properties'][i], prop, )
          p.data['all_properties'][i] = prop
      p.save()
