# Make our own testrunner that by default only tests our own apps
from django.conf import settings
from facebook_user import settings as fbu_setings
from django.test.simple import DjangoTestSuiteRunner


class ShopHappyTestRunner(DjangoTestSuiteRunner):
    def build_suite(self, test_labels, *args, **kwargs):
        PROJECT_APPS = []
        # Combine the list of apps form shop_happy and facebook_user
        TESTABLE_PROJECT_APPS = settings.PROJECT_APPS + fbu_setings.PROJECT_APPS
        # Remove path info and use only the app "label"
        for app in TESTABLE_PROJECT_APPS:
            PROJECT_APPS.append(app.split('.')[-1])
        return super(ShopHappyTestRunner, self).build_suite(test_labels or PROJECT_APPS, *args, **kwargs)
