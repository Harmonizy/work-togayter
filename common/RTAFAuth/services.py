import requests as rq
import json

from django.conf import settings

LDAP_url = settings.AIRFORCE_AUTHENTICATION.get("url",{}).get("AD","") 

RTAF_API_KEYCHAIN="55q5m5j3f4a4"
RTAF_API_ORGNAME="ศซว.ทอ."
RTAF_API_APIKEY="SGXDB5B6f7Q*X2"
RTAF_API_URL="http://10.229.22.2:8080/api/RTAFPerson"
RTAF_HOUSE_API_URL="http://10.229.22.2:8080/api/RTAFHousePerson"
super_app_auth_url = settings.AIRFORCE_AUTHENTICATION.get("url",{}).get("super_app","")
super_app_token = settings.AIRFORCE_AUTHENTICATION.get("super_app_token", "")


class ExternalAPIError(Exception): pass
class ExternalAPIInvalidResponse(ExternalAPIError): pass


class RTAFAPIService:
    @staticmethod
    def _call_api(url, payload_dict, apikey):
        payload = json.dumps(payload_dict)
        headers = {
            'APIKEY': apikey,
            'Content-Type': 'application/json'
        }

        try:
            print("Calling API with payload:", payload)
            print("API URL:", url)
            print("Headers:", headers)
            response = rq.post(url, headers=headers, data=payload, timeout=10)
        except rq.RequestException as e:
            raise ExternalAPIError(f"Connection error: {str(e)}")

        if response.status_code != 200:
            raise ExternalAPIError(f"API error {response.status_code}: {response.text}")

        try:
            data = response.json()
        except ValueError:
            raise ExternalAPIInvalidResponse("Invalid JSON response")

        if isinstance(data, list): # ✅ ตรวจว่าตอบกลับเป็น list และ item แรกมี ID เป็น "ไม่พบข้อมูล"
            if not data:
                raise ExternalAPIInvalidResponse("API response is an empty list")
            first_item = data[0]
            if isinstance(first_item, dict) and first_item.get("ID") == "ไม่พบข้อมูล":
                raise ExternalAPIError("ไม่พบข้อมูลในฐานข้อมูล กพ.ทอ.")

        return data

    @staticmethod
    def fetch_affiliation(org_short_name="ศซว.ทอ.", idc="", fname="", sername=""):
        payload = {
            "keychain": RTAF_API_KEYCHAIN,
            "orgname": org_short_name,
            "idc": idc,
            "fname": fname,
            "sername": sername
        }
        return RTAFAPIService._call_api(RTAF_API_URL, payload, RTAF_API_APIKEY)

    @staticmethod
    def fetch_person_detail(person_id="", email=""):
        if not person_id and not email:
            raise ValueError("ต้องระบุอย่างน้อย person_id หรือ email")

        payload = {
            "keychain": RTAF_API_KEYCHAIN,
            "idc": person_id,
            "em": email
        }
        
        return RTAFAPIService._call_api(RTAF_HOUSE_API_URL, payload, RTAF_API_APIKEY)
        

class AuthAPIService:
    @staticmethod
    def call_ad_auth_api(username: str, password: str):
        payload = json.dumps({
            "user": username,
            "pass": password
        })

        try:
            response = rq.post(LDAP_url, headers={'Content-Type': 'application/json'}, data=payload, timeout=10)
        except rq.RequestException as e:
            raise ExternalAPIError(f"Connection error: {str(e)}")

        if response.status_code != 200:
            raise ExternalAPIError(f"API error {response.status_code}: {response.text}")

        try:
            return response.json()
        except ValueError:
            raise ExternalAPIInvalidResponse("Invalid JSON response")
        
    @staticmethod
    def call_salt_auth_api(salt: str):
        headers = {
            "Content-Type": "application/json",
            "Gateway-key": f"Bearer {super_app_token}"
        }
        payload = json.dumps({"salt": salt})
        try:
            print("Salt service payload:", payload)
            print("headers:", headers)
            response = rq.post(super_app_auth_url, headers=headers, data=payload)
            print("Salt service response:", response)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise ExternalAPIError(f"Salt service error: {str(e)}")
        

from common.RTAFUser.models import Affiliation, Rank
def update_user_function_AD(user, response_data):
    
    user.is_active = True
    user.rank_id = response_data.get("rankID", 0)
    user.first_name = response_data.get("fname", "")
    user.last_name = response_data.get("lname", "")
    user.position = response_data.get("user_position", "")
    user.affiliation = Affiliation.objects.get_or_create(
                                                    short_name=response_data.get("user_orgname", ""),
                                                    defaults={
                                                        "full_name": response_data.get("user_orgname", "")
                                                    })[0]
    user.email = response_data.get("email", "")
    user.save()