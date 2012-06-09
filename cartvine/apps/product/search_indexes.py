# encoding: utf-8
from haystack import indexes
from models import Product


class ProductIndex(indexes.RealTimeSearchIndex, indexes.Indexable):
    """
    Realtimesearch handler for Products
    """
    text = indexes.CharField(document=True, use_template=True)
    provider_id = indexes.CharField(model_attr='provider_id')
    name = indexes.CharField(model_attr='name')
    slug = indexes.CharField(model_attr='slug')
    tags = indexes.CharField(model_attr='tags')
    featured_image_src = indexes.CharField(model_attr='featured_image_src',null=True)
    shop = indexes.CharField(model_attr='shop__name')
    shop_url = indexes.CharField(model_attr='shop__url')

    def get_model(self):
        return Product

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.select_related('shop').all()

