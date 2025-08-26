import logging

from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# from rest_framework.authtoken.models import Token


logger_success = logging.getLogger('django.security.login_success')
logger_failure = logging.getLogger('django.security.login_failure')

@receiver(user_logged_in)
def log_login_success(sender, request, user, **kwargs):
    logger_success.info(f'Login success: {user.username} - {user.get_full_name()}.')

@receiver(user_login_failed)
def log_login_failure(sender, credentials, request, **kwargs):
    username = credentials.get('username')
    logger_failure.warning(f'Login failure: {username}')
