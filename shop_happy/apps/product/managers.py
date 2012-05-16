from django.db import models


class ProductManager(models.Manager):

    def by_shopify_owner(self, user):
        """ apply the user customer/company filter to the recordset
        this method is called from the api AdcloudBaseModelResource """
        qs = self.get_query_set()
        try:
            qs = qs.filter(shop__users__in=[user])
        except AttributeError:
            pass

        return qs