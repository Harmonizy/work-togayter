from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings

from .api_auth import call_ad_login_authen, authen_api_to_RTAFUser
from common.RTAFUser.models.choices import DataStatus

User = get_user_model()

group_allow_mode_settings = settings.AF_AUTHENTICATION["group_allow_mode"]
bypass_setting = settings.AF_AUTHENTICATION.get("bypass_user", [])
allow_new_user = settings.AF_AUTHENTICATION.get("allow_new_user", False)

class SWCAuthBackend(BaseBackend):
    def is_allow_mode_for_user_group(self, user, mode):
        if user.is_superuser:
            return mode in group_allow_mode_settings["superuser"]
        else:
            for group in user.groups.all():
                if group.name in group_allow_mode_settings:
                    return mode in group_allow_mode_settings[group.name]
            else:
                return mode in group_allow_mode_settings["general"]
    
    def authenticate(self, request, username=None, password=None):
        # print("IP Address for debug-toolbar: " + request.META['REMOTE_ADDR'])     
        # print("Username: " + username)
        # print("bypass_setting: ", bypass_setting)
        # print("settings.DEBUG: ", settings.DEBUG)
        # print(settings.DEBUG and username in bypass_setting)
        if settings.DEBUG and username in bypass_setting:
            user, _ = User.objects.get_or_create(username=username)
            messages.warning(request, f"Bypass login for {username}")
            return user
        
        try:
            data = call_ad_login_authen(username, password)
            
            login_mode = data.get('login_mode', None)
            user, is_new = self.get_or_create_user(request, username, data)

            if is_new:
                user.is_active = allow_new_user
                user.save()
                if allow_new_user:
                    messages.success(request, f"สร้างผู้ใช้งานใหม่ {username}")
                else:
                    messages.info(request, f"สร้างผู้ใช้งาน {username} เรียบร้อย ติดต่อ Admin เพื่อขอสิทธิ์เข้าใช้งาน")
                    return None

            if not self.is_allow_mode_for_user_group(user, login_mode):
                raise Exception(f"login mode {login_mode} for this user is not allow")                        
            
            request.session['authen_token'] = data['token']            
            return user
        
        except Exception as e:
            messages.error(request, f"ผิดพลาด {e}")
            return None        
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
    def get_or_create_user(self, request, username, data):
        user, is_new = User.objects.get_or_create(username=username)
        if is_new:
            user, _ = authen_api_to_RTAFUser(data)
        elif user.data_status == DataStatus.EXTENSION:
            if user.login_limited == 0:
                messages.error(request, f"กรุณาแก้ไขข้อมูลส่วนตัวก่อนเข้าใช้งาน")
            else:
                user.login_limited -= 1
        return user, is_new