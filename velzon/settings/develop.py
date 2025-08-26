import os
import socket

from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]


INSTALLED_APPS += ["debug_toolbar",]
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

ip = socket.gethostbyname(socket.gethostname())

INTERNAL_IPS = ['127.0.0.1',  ip[:-1] + '1']

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://127.0.0.1:8000",
#     "http://localhost:5173",
# ]

# print("INSTALLED_APPS")
# print(INSTALLED_APPS)

# Uncomment for caching in development
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#     }
# }

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': os.getenv('CELERY_BROKER_URL', 'redis://redis_container:6379/0'),
#     }
# }

# # Celery configurations
# CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis_container:6379/0')
# CELERY_RESULT_BACKEND = CELERY_BROKER_URL