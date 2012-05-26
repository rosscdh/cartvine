from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.contrib.auth.models import User

from shop_happy.apps.customer.models import Customer

import logging
logger = logging.getLogger('facebook_user')


class CustomerView(View):
    queryset = Customer.objects.all()
    def post(self, request, *args, **kwargs):
		request_body = request.read()
		try:
		    body = request.POST
		    logger.debug('Person Validation Recieved: %s' %(body,) )
		except:
		    logger.error('Person Validation from shopify could not parse response body as JSON')

		user = authenticate(uid=body.get('fb_id'))
		# user, is_new = User.objects.get_or_create(username=username, email=body.get('email'))
		# if is_new:
		# 	user.set_unusable_password()
		# 	user.save()

		# person, is_new = Customer.objects.get_or_create(email=body.get('email'), shopify_id=body.get('fb_id'))
		# person.first_name = body.get('first_name')
		# person.last_name = body.get('last_name')
		# person.data = body.get('data')
		# person.save()

		if is_new:
			logger.info('Create New Facebook Person: %s' %(person.get_full_name,) )
		else:
			logger.info('Returning Facebook Person: %s' %(person.get_full_name,) )

		# login(request, request.user)

		return HttpResponse(status=200)
