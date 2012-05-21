from django.db import models
from jsonfield import JSONField

from shop_happy.apps.shop.models import Shop
from shop_happy.apps.customer.models import Customer

from managers import ShopHappyEmailManager

import datetime
from dateutil import parser


class ShopHappyEmail(models.Model):
    shop = models.ForeignKey(Shop)
    customer = models.ForeignKey(Customer, related_name='target_customer')
    email_to = models.EmailField()
    post_date = models.DateField()
    sent_date = models.DateField(null=True,blank=True)
    data = JSONField()

    objects = ShopHappyEmailManager()

    def __unicode__(self):
    	return u'%s on %s - set ' %(self.email_to, self.post_date,)

    def get_customer_full_name(self):
    	return u'%s %s' %(self.data['customer']['first_name'], self.data['customer']['last_name'],)

    @staticmethod
    def get_email_post_date(date_from=None):
        date_difference = datetime.timedelta(weeks=2)

        if date_from is None:
            date_from = datetime.date.today()
        else:
            date_from = parser.parse(date_from)

        return date_from + date_difference

