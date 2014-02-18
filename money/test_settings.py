import os

TEST_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tests')


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(TEST_DIR, 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = (
    'money',
    'money.tests',
)

SECRET_KEY = 'abcde12345'


CACHES = {
    # No cache
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

FIXTURE_DIRS = ('../money/contrib/django/tests/fixtures/',)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
)

