try:
    from .base import *
except ImportError:
    print('Unable to import base settings file.')

print('Using locally native server (sqlite3)')
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(RUN_ROOT, 'db.sqlite3'),
        'CONN_MAX_AGE': 600,  # 10 Minutes
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
