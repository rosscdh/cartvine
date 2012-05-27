from django.conf import settings
from django.contrib.auth.models import User

from models import Person

import logging
logger = logging.getLogger('facebook_user')


class PersonFacebookBackend(object):
    """
    Log the user in if we have a user object
    and we have a FB uid and access_token
    """
    supports_inactive_user = True

    def authenticate(self, user, application_type, uid, access_token):
        logger.info('user: %s, application_type: %s, uid: %s, access_token: %s'%(user, application_type, uid, access_token))

    	person, is_new = Person.objects.get_or_create(application_type=application_type, uid=uid)

        person.access_token=access_token
        person.user = user
        person.save()

        return person.user

    def get_user(self, user_id):
        """ retrieve user account from related adcloudUser 
        and not the base django user
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
