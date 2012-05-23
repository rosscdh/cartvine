from django.db import models
from jsonfield import JSONField

from shop_happy.apps.shop.models import Shop
from managers import ProductManager


class Product(models.Model):
    shop = models.ForeignKey(Shop)
    shopify_id = models.IntegerField(db_index=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    data = JSONField()

    objects = ProductManager()

    def __unicode__(self):
        return u'%s' % (self.slug,)

    @property
    def summary(self):
        return u'%s' % (self.data['body_html'],)

    @property
    def product_type(self):
        return u'%s' % (self.data['product_type'],)

    @property
    def shopify_url(self):
        return u'/admin/products/%d' % (self.shopify_id,)

    @property
    def shopify_updated_at(self):
        return self.data['updated_at'] if 'updated_at' in self.data and not None else None

    @property
    def featured_image_src(self):
        return self.data['featured_image'] if 'featured_image' in self.data else None

    def get_images_src(self):
        return self.data['images'] if 'images' in self.data and isinstance(self.data['images'], type([])) else None
