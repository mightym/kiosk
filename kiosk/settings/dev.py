from .base import *


DEBUG = True
TEMPLATE_DEBUG = True
COMPRESS_ENABLED = False
THUMBNAIL_PRESERVE_FORMAT = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {'format': '%(levelname)s %(asctime)s %(name)s %(message)s'},
        'short': {'format': '%(levelname)s %(asctime)s %(message)s'},
        'verbose': {'format': '%(levelname)s %(asctime)s %(name)s %(message)s\n%(request)s'},
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'short',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'omnibus': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}



try:
    from .local import *
except ImportError:
    pass
