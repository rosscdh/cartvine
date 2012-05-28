from celery.task import task
from django.conf import settings
from django.template.defaultfilters import slugify

from PIL import Image
import urllib2
from django.core.files.base import ContentFile
from StringIO import StringIO

from cartvine.apps.shop.models import Shop
from models import Product

from urlparse import urlparse
import shopify
import logging
logger = logging.getLogger('happy_log')


@task(name="sync_products")
def sync_products(shopify_session, shop):
    """ Task to sync the products listed in Shopify shop with local database 
    Called on login/install """

    shop.activate_shopify_session()

    try:
        latest_product = Product.objects.filter(shop=shop).latest('shopify_id')
    except Product.DoesNotExist:
        # No Products stored locally so simple get them all from the shop
        logger.info('No Products stored locally for %s so get all from the Shopify API'%(shop,))

        latest_product = None
        shopify_products = shopify.Product.find()

    if latest_product:
        shopify_products = shopify.Product.find(since_id=latest_product.shopify_id)
        if latest_product.shopify_updated_at:
            shopify_products += shopify.Product.find(updated_at_min=latest_product.shopify_updated_at)

    if shopify_products:

        logger.info('%d new Products found for %s' %(len(shopify_products),shop,))

        for product in shopify_products:
            # should use get_or_create here?
            safe_attribs = product.__dict__['attributes']
            safe_attribs['variants'] = None
            safe_attribs['options'] = None
            safe_attribs['featured_image'] = product.attributes['images'][0].attributes['src'] if len(product.attributes['images']) > 0 else None
            safe_attribs['images'] = []

            if len(product.attributes['images']) > 0:
                for i in product.images:
                    safe_attribs['images'].append(i.attributes['src'])

            p, is_new = Product.objects.get_or_create(shop=shop, shopify_id=product.id)
            p.data = safe_attribs
            p.name = product.title
            p.slug = slugify(product.title)
            p.save()

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