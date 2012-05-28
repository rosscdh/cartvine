from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.utils import simplejson as json


from socialregistration.views import Setup
from socialregistration.contrib.facebook.client import Facebook as FacebookClient
from socialregistration.contrib.facebook.models import FacebookProfile

from models import Person

import logging
logger = logging.getLogger('facebook_user')


class PersonValidationView(View):

    def post(self, request, application_type):

        if not Person.APPLICATION_TYPES.is_valid(application_type):
            logger.error('Not a valid application_type: %s'%(application_type))
            raise Http404

        request_body = request.read()
        response_data = {}
        try:
            body = json.loads(request_body)
            logger.debug('Person Validation Recieved: %s' %(body,) )
        except:
            logger.error('Person Validation from facebook javascript client, but could not parse response body as JSON')
            raise Http404

        if request.user.is_authenticated():
            logger.debug('Person Validation not necessary, user is logged in already : %s'%(request.user))    
        else:

            if body.get('uid') is not None and body.get('access_token') is not None:

                uid = body.get('uid')
                access_token = body.get('access_token')
                username = body.get('username')
                email = body.get('email')
                first_name = body.get('first_name')
                last_name = body.get('last_name')
                logger.info('Person uid: %s access_token: %s' %(uid, access_token,) )

                user, is_new = User.objects.get_or_create(username=username, email=email, first_name=first_name, last_name=last_name)
                user = authenticate(user=user, application_type=Person.APPLICATION_TYPES.facebook, uid=uid, access_token=access_token)

                if user is None:
                    logger.error('Person was meant to be created, but was not: application_type: %s, uid: %s, access_token: %s'%(application_type, uid, access_token))
                    raise Http404
                else:
                    user.data = body
                    user.save()

                    # @TODO make this dynamic when more than jsut FB is supported
                    # Abstract into seperate class
                    client = FacebookClient()
                    profile, is_new = FacebookProfile.objects.get_or_create(user=user, uid=uid)
                    logger.info('New Facebook Profile Person uid: %s access_token: %s' %(uid, access_token,) )

                    # @TODO bug here can pass and uid and or access token in.. need to call facebook to validate here
                    if user is not None and hasattr(user, 'data'):
                        user.data = body

                    request.session['next'] = reverse('default:index')

                    login(request, user)

                response_data = request.user.person.get_validated_json_response()

        return HttpResponse(json.dumps(response_data), mimetype="application/json")
