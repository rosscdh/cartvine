from django.db import models


class CustomerManager(models.Manager):

    def apply_api_user_filter(self, user):
        """ apply the user customer/company filter to the recordset
        this method is called from the api AdcloudBaseModelResource """
        qs = super(CustomerManager, self).get_query_set()
        try:
            qs = qs.filter(pk=user.pk)
        except AttributeError:
            pass

        return qs

    def by_shopify_owner(self, user):
        """ apply the user customer/company filter to the recordset
        this method is called from the api AdcloudBaseModelResource """
        qs = self.get_query_set()
        try:
            qs = qs.filter(shop__users__in=[user])
        except AttributeError:
            pass

        return qs
