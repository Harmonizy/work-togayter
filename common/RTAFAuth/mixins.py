import json

from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.module_loading import import_string

import requests as rq

from common.RTAFUser.models.RTAFUser import Affiliation

from .services import RTAFAPIService, AuthAPIService, ExternalAPIError


LDAP_url = settings.AIRFORCE_AUTHENTICATION.get("url",{}).get("AD","") 
HRIS_url = settings.AIRFORCE_AUTHENTICATION.get("url",{}).get("HRIS","")
allow_mode = settings.AIRFORCE_AUTHENTICATION.get("allow_mode", ["SWC-AUTH-Login",])
default_is_active = settings.AIRFORCE_AUTHENTICATION.get("default", {}).get("is_active", False)

UserModel = get_user_model()


class GetUserMixins:
    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


class AuthAPIMixin:
    def call_auth_api(self, username, password):
        try:
            result = AuthAPIService.call_ad_auth_api(username, password)
            return result
        except ExternalAPIError as e:
            return {"error": str(e)}
        
    def is_auth_success(self, request, response_data):
        print("Authentication response:", response_data)
        if response_data.get("result") == "Process-Complete":
            if response_data.get("login_mode") in allow_mode:
                print("Login mode allowed:", response_data.get("login_mode"))
                return True
            else:
                messages.error(request, f"ไม่อนุญาตให้ login mode ด้วย {response_data.get('login_mode')}")
        return False

    def store_token_to_session(self, request, response_data):
        token = response_data.get("token")
        if request and token:
            request.session["rtaf_token"] = token
            

class UserSyncMixin:   

    def update_or_create_user(self, user_model, response_data, username):
        user, created = user_model.objects.get_or_create(username=username)
        
        user.is_active = default_is_active
        
        updater_path = getattr(settings, "AIRFORCE_AUTHENTICATION", {}).get("update_user_function_AD", None)
        
        if updater_path:
            updater = import_string(updater_path)
            if callable(updater):
                updater(user, response_data)
            
        return user


class HRISDataMixin:
    def call_hris_api(self, token, email = "", person_id = ""):
        try:
            result = RTAFAPIService.fetch_person_detail(email=email, person_id=person_id)
            return result
        except ExternalAPIError as e:
            return {"error": str(e)}


class SaltAuthMixin:
    """Mixin for handling salt-based authentication"""
    
    def _get_user_info_from_salt(self, salt):
        reponse = AuthAPIService.call_salt_auth_api(salt)
        return reponse
    

    def _get_or_create_user(self, user_info):
        UserModel = get_user_model()
        mfa_data = user_info.get("mfa_data", {})
        username = user_info["user"].lower().strip()
        
        user, _ = UserModel.objects.get_or_create(
            username=username,
            defaults={
                "first_name": mfa_data.get("fname", ""),
                "last_name": mfa_data.get("lname", ""),
                "email": f"{username}@rtaf.mi.th",
                "rank_id": mfa_data.get("rankID", ""),
                "person_id": user_info.get("citizen_id", ""),
                "af_id": user_info.get("airforce_id", ""),                
                "position": mfa_data.get("user_position", ""),
                "affiliation": Affiliation.objects.get_or_create(short_name=mfa_data.get("user_orgname", ""))[0],
            }
        )
        print("User created or fetched:", user)
        return user
