from django.conf import settings
from django.contrib.auth.models import User




class ShopifyUserBackend(object):
    """
    Log the user in if we have a user object
    and we have an access_token
    """
    supports_inactive_user = False

    def authenticate(self, user=None, access_token=None):
        if user is None:
            return None
        if access_token is None:
            return None

        return user

    def get_user(self, user_id):
        """ retrieve user account from related adcloudUser 
        and not the base django user
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
