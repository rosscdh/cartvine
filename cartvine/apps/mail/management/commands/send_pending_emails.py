import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from optparse import make_option

from cartvine.apps.mail.models import ShopHappyEmail

from templated_email import send_templated_mail

import datetime
from dateutil import parser

import logging
logger = logging.getLogger('happy_log')


class Command(BaseCommand):
    args = '<page_id page_id ...>'
    help = 'Manage the Cuttingroom Floor: --delete'
    option_list = BaseCommand.option_list + (
        make_option('--addresses',
            action='store_true',
            dest='addresses',
            default=False,
            help='List of email addresses in db to send for'),
        make_option('--dateof',
            action='store_true',
            dest='dateof',
            default=False,
            help='Specific date to send emails for (yyyy-mm-dd)'),
        )

    needle = None

    def handle(self, *args, **options):
        

        if options['dateof']:
            self.dateof = parser.parse(args[0])
        else:
            self.dateof = datetime.date.today()


        email_list = ShopHappyEmail.objects.select_related('shop').filter(post_date=self.dateof)

        for email in email_list:
            send_templated_mail(
                template_name='invitation_to_review',
                from_email='ross@tweeqa.net',
                recipient_list=[email.data['customer']['email']],
                context={
                    'shop': email.shop,
                    'name': email.get_customer_full_name(),
                    'product_list': email.data['line_items'],
                },
                headers={'My-Custom-Header':'Custom Value'}
            )