#!/usr/bin/env python
import sys

# Bootstrap Django's settings.
from django.conf import settings
if not settings.configured:
    settings.configure(
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                #'NAME': 'python-money-test'
                'NAME': ':memory;'
            }
        },
        INSTALLED_APPS=[
            'money',
            'money.tests',
        ],
        TEST_RUNNER = "django_nose.NoseTestSuiteRunner",
    )

def runtests():
    """Test runner for setup.py test."""
    import django.test.utils
    runner_class = django.test.utils.get_runner(settings)
    test_runner = runner_class(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['money'])

    # The following is a hack around a bug
    sys.exitfunc = lambda: 0
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
