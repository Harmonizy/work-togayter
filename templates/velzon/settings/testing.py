import os
import socket

from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "testing-db.sqlite3",
    }
}

INSTALLED_APPS += ["debug_toolbar",]
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

ip = socket.gethostbyname(socket.gethostname())

INTERNAL_IPS = ['127.0.0.1',  ip[:-1] + '1']

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
]

AUTH_USER_MODEL = 'RTAFUser.RTAFUser'
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend', ]

# Uncomment for caching in development
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#     }
# }
