'''Production Use Settings File'''
try:
    from .base import *
except ImportError as e:
    raise Exception("A base.py file is required to run this project")


# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS += ['http://domain.com', '*']

# Gmail Email Configuration!
EMAIL_BACKEND = env.str("APP_EMAIL_BACKEND")
EMAIL_HOST = env.str("APP_EMAIL_HOST")
EMAIL_HOST_USER = env.str("APP_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("APP_EMAIL_HOST_PASSWORD")
EMAIL_USE_LOCALTIME = env.bool("APP_EMAIL_USE_LOCALTIME")
EMAIL_PORT = env.int("APP_EMAIL_PORT")
EMAIL_USE_TLS = env.bool("APP_EMAIL_USE_TLS")
DEFAULT_FROM_EMAIL = env.str("APP_DEFAULT_FROM_EMAIL")
SERVER_EMAIL = env.str("APP_SERVER_EMAIL")
EMAIL_FROM_NAME = f"B-Web Admin <{EMAIL_HOST_USER}>"
BASE_URL = env.str("APP_BASE_URL")

SENDGRID_SANDBOX_MODE_IN_DEBUG = False
SENDGRID_ECHO_TO_STDOUT = False

INSTALLED_APPS += [
    'health_check',                             # required
    'health_check.db',                          # stock Django health checkers
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.celery',              # requires celery
    # disk and memory utilization; requires psutil
    'health_check.contrib.psutil',
    # requires boto and S3BotoStorage backend
    'health_check.contrib.s3boto_storage',
    'health_check.contrib.rabbitmq',
]

CORS_ALLOW_CREDENTIALS = True
# CORS_ORIGIN_ALLOW_ALL = True
# CORS_URLS_REGEX = r'^/api.*$'
# CORS_ORIGIN_WHITELIST = ('*',)
CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://localhost:8080',
)

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

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

NOCAPTCHA = True
# RECAPTCHA_PROXY = 'http://127.0.0.1:8000'
RECAPTCHA_PUBLIC_KEY = CONFIG('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = CONFIG('RECAPTCHA_PRIVATE_KEY')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'KEY_PREFIX': f"myapp-{os.environ.get('ENV')}",
        'LOCATION': [
            'cz01:11212',
            'cz02:11212',
            'cz03:11212',
        ],
        'TIMEOUT': 60,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
            'server_max_value_length': 1024 * 1024 * 2  # 2MB
        }
    }
}

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 86400  # set just 30 minutes to test
SESSION_SAVE_EVERY_REQUEST = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE.insert(  # insert WhiteNoiseMiddleware right after SecurityMiddleware
    MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') + 1,
    'whitenoise.middleware.WhiteNoiseMiddleware')

# django-log-request-id
MIDDLEWARE.insert(  # insert RequestIDMiddleware on the top
    0, 'log_request_id.middleware.RequestIDMiddleware')

# Celery
CELERY_BROKER_URL = 'amqp://user:password@mz01:5672/myvhost' # 'CONFIG('REDIS_URL')
CELERY_RESULT_BACKEND = 'amqp://user:password@mz01:5672/myvhost' # 'CONFIG('REDIS_URL')
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Jerusalem'

LOG_REQUEST_ID_HEADER = 'HTTP_X_REQUEST_ID'
GENERATE_REQUEST_ID_IF_NOT_IN_HEADER = True
LOG_REQUESTS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        },
    },
    'formatters': {
        'standard': {
            'format': '%(levelname)-8s [%(asctime)s] [%(request_id)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['request_id'],
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'log_request_id.middleware': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}