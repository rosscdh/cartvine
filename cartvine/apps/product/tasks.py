from celery.task import task
from django.conf import settings
from django.template.defaultfilters import slugify

from PIL import Image
import urllib2
from django.core.files.base import ContentFile
from StringIO import StringIO

from cartvine.apps.shop.models import Shop
from cartvine.apps.product.models import Product, ProductVariant

from urlparse import urlparse
import shopify
import logging
logger = logging.getLogger('happy_log')


@task(name="sync_products")
def sync_products(shop):
    """ Task to sync the products listed in Shopify shop with local database 
    Called on login/install """

    shop.activate_shopify_session()

    try:
        latest_product = Product.objects.filter(shop=shop).latest('provider_id')
    except Product.DoesNotExist:
        # No Products stored locally so simple get them all from the shop
        logger.info('No Products stored locally for %s so get all from the Shopify API'%(shop,))

        latest_product = None
        shopify_products = shopify.Product.find()

    if latest_product:
        shopify_products = shopify.Product.find(since_id=latest_product.provider_id)
        if latest_product.shopify_updated_at:
            shopify_products += shopify.Product.find(updated_at_min=latest_product.shopify_updated_at)

    if shopify_products:

        logger.info('%d new Products found for %s' %(len(shopify_products),shop,))

        for product in shopify_products:
            # should use get_or_create here?
            safe_attribs = product.__dict__['attributes']
            safe_attribs['variants'] = [v.attributes for v in product.variants]
            safe_attribs['options'] = [o.attributes for o in product.options]
            safe_attribs['featured_image'] = product.attributes['images'][0].attributes['src'] if len(product.attributes['images']) > 0 else None
            if len(product.attributes['images']) > 0:
                safe_attribs['images'] = [i.attributes['src'] for i in product.attributes['images']]
            else:
                safe_attribs['images'] = []

            p, is_new = Product.objects.get_or_create(shop=shop, provider_id=product.id)
            p.data = safe_attribs
            p.name = product.title
            p.slug = slugify(product.title)
            if not p.has_basic_properties:
                p.reset_basic_properties()
            p.save()

            # Do variants
            for v in product.variants:
                pv, is_new = ProductVariant.objects.get_or_create(product=p, provider_id=v['id'])
                pv.sku = v['sku']
                pv.inventory_quantity = v['inventory_quantity']
                pv.position = v['position']
                pv.data = v
                pv.save()

    return None


@task(name="set_variant_order")
def set_variant_order():
    """ Task make all product variants order by their position argument """
    logger.info('Start Task: set_variant_order')

    for v in ProductVariant.objects.all():
        if 'position' in v.data:
            v.position = v.data['position']
            v.save()
        else:
            logger.warn('No "position" key found in Variant.data variant(%d)'%(v.pk,))            


    return None


REMOTE_IMAGE_STORAGE_PATH = getattr(settings, 'REMOTE_IMAGE_STORAGE_PATH', 'remote')
@task(name="retrieve_remote_image")
def retrieve_remote_image(src):
    """ Method downloads and saves a remote image based on its url
    then returns a local url or false if unable to download and save
    """
    logger.info('Starting download of Remote Image: %s' %(src,))
    image = urlparse(src)
    if not image.scheme in ['http','https']:
        logger.error('Could not download Image from : %s - Incorrect Scheme' %(src,))
    else:
        # valid scheme continue with process
        # open remote image
        output_file = '%s/%s' % (settings.MEDIA_ROOT, REMOTE_IMAGE_STORAGE_PATH,)
        name = 'test'
        input_file = StringIO(urllib2.urlopen(src).read())
        output_file = StringIO()
        img = Image.open(input_file)
        if img.mode != "RGB":
            img = img.convert("RGB")
        # save file locally
        img.save(output_file, "JPEG")
        image.save(name+".jpg", ContentFile(output_file.getvalue()), save=False)

    return None
