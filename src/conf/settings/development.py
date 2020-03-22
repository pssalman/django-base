'''Development Use Settings File'''
try:
    from .base import *
except ImportError as e:
    raise Exception("A base.py file is required to run this project")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS += ['127.0.0.1', 'localhost']

# Django Mail Backend Service to Use With Development
EMAIL_BACKEND = env.str("APP_EMAIL_BACKEND")
EMAIL_SUBJECT_PREFIX = env.str("APP_EMAIL_SUBJECT_PREFIX")
DEFAULT_FROM_EMAIL = env.str("APP_DEFAULT_FROM_EMAIL")
EMAIL_HOST_USER = env.str("APP_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("APP_EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env.bool("APP_EMAIL_USE_TLS")
EMAIL_PORT = env.int("APP_EMAIL_PORT")

print('Using postgresql on docker container ...')
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': env.str("APP_DB_ENGINE"),
        'NAME': env.str("APP_DB_NAME"),
        'USER': env.str("APP_DB_USER"),
        'PASSWORD': env.str("APP_DB_PASSWORD"),
        'HOST': env.str("APP_DB_HOST"),
        'PORT': env.str("APP_DB_PORT"),
        'CONN_MAX_AGE': env.int("APP_DB_CONN_MAX_AGE"),
        'ATOMIC_REQUESTS': env.bool("APP_DB_ATOMIC_REQUESTS"),
    }
}

INSTALLED_APPS += [
    'health_check',                             # required
    'health_check.db',                          # stock Django health checkers
    'health_check.cache',
]

CORS_ALLOW_CREDENTIALS = False
CORS_ORIGIN_ALLOW_ALL = True
#CORS_URLS_REGEX = r'^/api.*$'
#CORS_ORIGIN_WHITELIST = ('*',)
# CORS_ORIGIN_WHITELIST = (
#    'http://localhost:3000',
#    'http://localhost:8080',
# )

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1800  # set just 30 minutes to test
SESSION_SAVE_EVERY_REQUEST = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

NOCAPTCHA = True
# RECAPTCHA_PROXY = 'http://127.0.0.1:8000'
#RECAPTCHA_PUBLIC_KEY = CONFIG('RECAPTCHA_PUBLIC_KEY')
#RECAPTCHA_PRIVATE_KEY = CONFIG('RECAPTCHA_PRIVATE_KEY')

CELERY_BROKER_URL = 'amqp://user:password@mz01:5672//'
CELERY_RESULT_BACKEND = 'redis://rz01:6379/0'
CELERY_TIMEZONE = 'Asia/Jerusalem'

# Celery
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

ROSETTA_SHOW_AT_ADMIN_PANEL = True
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
YANDEX_TRANSLATE_KEY = 'trnsl.1.1.20190815T224127Z.0086df2fbe68214e.cc585370662543e088d38d5ccbca1c99591aa26d'