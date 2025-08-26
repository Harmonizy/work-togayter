from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.conf import settings

from .mixins import (GetUserMixins, AuthAPIMixin, UserSyncMixin, HRISDataMixin, SaltAuthMixin)

UserModel = get_user_model()

class BaseRTAFBackend(GetUserMixins, AuthAPIMixin, UserSyncMixin, ModelBackend):

    def base_authenticate(self, request, username, password):
        username = username.strip().lower()
        if username in settings.AIRFORCE_AUTHENTICATION["bypass_user"] and settings.DEBUG:
            print("Bypassing authentication for user:", username)
            user = UserModel.objects.filter(username=username).first()
            if not user:
                user = UserModel.objects.create(username=username, is_active=True)
            return user, None
        response_data = self.call_auth_api(username, password)

        if not self.is_auth_success(request, response_data): 
            print("Authentication failed for username:", username)
            return None, response_data

        user = self.update_or_create_user(UserModel, response_data, username)
        self.store_token_to_session(request, response_data)

        return user, response_data


class RTAFLDAPBackend(BaseRTAFBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print("LDAP Backend for username:", username)
        user, _ = self.base_authenticate(request, username, password)
        return user


class HRISBackend(HRISDataMixin, BaseRTAFBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print("HRIS Backend for username:", username)
        user, response_data = self.base_authenticate(request, username, password)
        if not user: return None

        token = response_data.get("token", "")
        email = response_data.get("user") 
        if token and email and user.fetch_hris:
            hris_response = self.call_hris_api(token, email + "@rtaf.mi.th")
            if hris_response.get("result") == "Process-Complete":
                self.update_user_from_hris(user, hris_response)

        return user


class SuperAppBackend(GetUserMixins, SaltAuthMixin, ModelBackend):
    AUTH_USERNAME = "super-app-salt-auth"

    def authenticate(self, request, username=None, password=None, **kwargs):
        
        print("SuperAppSaltAuthBackend authenticate called : ", username, password)
        if username != self.AUTH_USERNAME or not password: return None
        user_info = self._get_user_info_from_salt(password)
        print("User info from salt:", user_info)
        if not user_info or "user" not in user_info: return None
        request.session["Token"] = user_info.get("mfa_data",{}).get("token","")
        request.session["payload"] = user_info.get("payload", {})
        print("user_info:", user_info)
        return self._get_or_create_user(user_info)
    
    
    