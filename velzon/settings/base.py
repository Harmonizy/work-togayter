import os
from pathlib import Path
from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent.parent


SECRET_KEY = 'djnseyq%^*3ldt_0krq5angab3i-#curo-7aggoecxw!d-j^gke5w17&0w06+qf8+8'

DEBUG = True

ALLOWED_HOSTS = []


DEFAULT_APPS = [    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    ]

LOCAL_APPS = [
    "dashboards",
    "apps",
    "layouts",
    "components",
    "pages",
    
    "safety.Data",
    "safety.Report",
    "safety.RiskManagement",
    "safety.Evaluate",
    'safety.Dashboard',
]

COMMON_APPS = [
    'common.Configurations',
    'common.RTAFUser',
    'common.RTAFAuth',
    'common.Services',
    'common.SuperAppQR',
]

THIRDPARTY_APPS = [
    
    # Crispy Forms
    "crispy_forms",
    'crispy_bootstrap5',
    
    # All Auth
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    
    # 'allauth.socialaccount.providers.google',      
    # Google Providers
    'multiselectfield',
    'taggit',
    'ckeditor',
    "template_partials",
    "rules",
]

INSTALLED_APPS = DEFAULT_APPS + LOCAL_APPS + COMMON_APPS + THIRDPARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'velzon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]


ADMIN_URL_PATH = os.getenv('ADMIN_URL_PATH')
ADMIN_SITE_HEADER = os.getenv('ADMIN_SITE_HEADER')
ADMIN_INDEX_TITLE = os.getenv('ADMIN_INDEX_TITLE')
ADMIN_SITE_TITLE = os.getenv('ADMIN_SITE_TITLE')


AUTH_USER_MODEL = 'RTAFUser.RTAFUser'

AUTHENTICATION_BACKENDS = [
    'common.RTAFAuth.backends.SuperAppBackend',
    'common.RTAFAuth.backends.RTAFLDAPBackend',
    'common.RTAFAuth.backends.HRISBackend',
    'django.contrib.auth.backends.ModelBackend', 
    # 'allauth.account.auth_backends.AuthenticationBackend',
]

from common.RTAFAuth.settings import *
# from .rest_framework_settings import *

SUPER_APP_QR_PREFIX = os.getenv('SUPER_APP_QR_PREFIX',)

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

WSGI_APPLICATION = 'velzon.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DATABASE_NAME', os.path.join(os.path.dirname(__file__), 'db.sqlite')),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]



LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Bangkok'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,"static")]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.mailtrap.io"
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
DEFAULT_FROM_EMAIL = ""

LOGIN_URL = "account_login"
# LOGOUT_REDIRECT_URL = "/"


LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "account_login"
LOGOUT_REDIRECT_URL = "/login"
ACCOUNT_LOGOUT_ON_GET = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS =True

ACCOUNT_UNIQUE_EMAIL = True
SOCIALACCOUNT_LOGIN_ON_GET = True


ACCOUNT_FORMS = {
    "login": "velzon.forms.UserLoginForm",
    "signup": "velzon.forms.UserRegistrationForm",
    "change_password": "velzon.forms.PasswordChangeForm",
    "set_password": "velzon.forms.PasswordSetForm",
    "reset_password": "velzon.forms.PasswordResetForm",
    "reset_password_from_key": "velzon.forms.PasswordResetKeyForm",
}

SOCIALACCOUNT_QUERY_EMAIL = True

SITE_ID = 2

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

from .logging_settings import *
