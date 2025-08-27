import os
import socket

from .base import *

DEBUG = False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

CSRF_TRUSTED_ORIGINS = [
    'https://safety-analysis.rtaf.mi.th',
]

INSTALLED_APPS += ["debug_toolbar",]
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

ip = socket.gethostbyname(socket.gethostname())

INTERNAL_IPS = ['127.0.0.1',  ip[:-1] + '1']

# Redis caching (uncomment if used)
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': os.getenv('REDIS_URL', 'redis://redis:6379/1'),
#     }
# }

# Celery configurations
# CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
# CELERY_RESULT_BACKEND = CELERY_BROKER_URL
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = 'DENY'
