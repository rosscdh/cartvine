#!/usr/bin/env python
import os
import sys
from django.core.exceptions import ImproperlyConfigured
from cartvine.utils import get_namedtuple_choices

VALID_APPLICATIONS = get_namedtuple_choices('VALID_APPLICATIONS', (
    (['cartvine', 'core', 'cv', 'c'], 'cartvine', 'cartvine'),
    (['facebook_user', 'fbu', 'fb', 'f'], 'facebook_user', 'facebook_user'),
))


if __name__ == "__main__":
    """ We assume that the first argument will always be the application to run """
    try:
        application = sys.argv[1]
        for names,app in VALID_APPLICATIONS.get_choices():
            if application in names:
                application = app
                break
    except IndexError:
        app_names,application = VALID_APPLICATIONS.get_choices()[0]
        print 'Using %s Application as you did not specify an application in %s'%(application, VALID_APPLICATIONS,)

    if application not in VALID_APPLICATIONS.get_values():
        print '%s is not a valid application %s'%(application, VALID_APPLICATIONS,)
        application = VALID_APPLICATIONS.get_choices()[0]
    else:
        print 'Using %s Application'%(application,)
        try:
            sys.argv.pop(1)
        except IndexError:
            pass


    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings"%(application,))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
