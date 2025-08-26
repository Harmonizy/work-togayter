import requests as rq
import json

from django.contrib.auth import get_user_model
from django.conf import settings

from common.RTAFUser.models import Rank, Affiliation
from common.RTAFUser.models.choices import DataStatus

login_limited = settings.AF_AUTHENTICATION["login_limited"]
ad_url = settings.AF_AUTHENTICATION["ad_url"]
hris_url = settings.AF_AUTHENTICATION["hris_url"]

def call_ad_login_authen(username = None, otp = None):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "user": username,
        "pass": otp
    }

    try:
        response = rq.post(ad_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()        
        print("="*50)
        for k, v in data.items():
            print(f"{k} : {v}")
        print("="*50)
        if data['result'] == 'Process-Error':
            raise Exception("::".join(data['error']) if isinstance(data['error'], list) else data['error'])        
        return data
    except rq.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def authen_api_to_RTAFUser(api_response):
    RTAFUser = get_user_model()
    user, created = RTAFUser.objects.get_or_create(username=api_response['user'])

    user.first_name = api_response['fname']
    user.last_name = api_response['lname']
    user.position = api_response['user_position']
    user.af_id = api_response['user_id'] if 'user_id' in api_response else None

    if len(api_response['rankID']) == 5:
        rank, _ = Rank.objects.get_or_create(id=api_response['rankID'], short_name=api_response['rank'])
        user.rank = rank   
    if len(api_response['rankID']) < 5:
        user.data_status = DataStatus.EXTENSION
        user.login_limited = login_limited

    affiliation, _ = Affiliation.objects.get_or_create(short_name=api_response['user_orgname'], hris_code=api_response['user_orgname_code'])
    user.affiliation = affiliation
    user.work_affiliation = affiliation

    user.save()

    return user, created


def fetch_person_data(token, **kwargs):
    
    headers = {"Content-Type": "application/json"}
    try:
        response = rq.post(hris_url, json={"token": token, **kwargs}, headers=headers)
        response.raise_for_status()
        result = response.json()
        if result['result'] == 'Process-Complete':
            return result['data'][0] if result['data'] else {}
        raise Exception(result)

    except rq.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise e


def person_data_by_email(token, email):
    return fetch_person_data(token, email=email + "@rtaf.mi.th")


def person_data_by_person_id(token, person_id):
    return fetch_person_data(token, national_id=person_id)


def save_person_to_RTAFUser(person, username):
    RTAFUser = get_user_model()
    user, created = RTAFUser.objects.get_or_create(username=username)

    user.rank_id = person['RANKID']
    user.first_name = person['FIRSTNAME']
    user.last_name = person['LASTNAME']
    user.position = person['POSITION']
    user.af_id = person['ID']
    user.person_id = person['PEOPLEID']

    affiliation, _ = Affiliation.objects.get_or_create(short_name=person['UNITNAME'], hris_code=person['UNITCODE'])
    user.affiliation = affiliation
    user.work_affiliation = affiliation
    user.save()
    return user, created


def run_main():
    username = input("Enter  username : ")
    otp = input("Enter pongthep OTP : ")
    data = call_ad_login_authen(username, otp)
    authen_token = data['token']
    # print(data)
    authen_api_to_RTAFUser(data)
    person = person_data_by_email(authen_token, data['user'])
    # person = person_data_by_person_id(authen_token, person_id)
    save_person_to_RTAFUser(person, data['user'])

if __name__ == "__main__":
    run_main()
