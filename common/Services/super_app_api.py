import requests
import json
from typing import List

API_URL = "https://apigw.rtaf.mi.th/super-apps/api-notification-v1/push-notification-to-app"
GATEWAY_KEY = "Bearer 2Fg0lC4ye5l9hXG32t27EjOY-ROSyrX_2a1LseEc1veSWAcaLigCWvcvVhKyXFVyWLMDnqP4y8FCSw-fCNKg2Rf5mlwuFYVFDI9JoyYgNn2w598TNZoJagVpjtLvkQkm1czYNIvQpCUpQHTQQSkC85Ju64iGQ_tb0rrg8okZFx_t3dS-9Hd10Xhuku9MbEi2biYX-CdxEQzm0dxLHYY3bqQ9J3DDFhoS_eS4uBD5x5TfdzB64HyOC9tMvqKEnWXGEXNRKSQsj-A"
COOKIE_SESSION = "cookiesession1=678A8C328D216FD4FC0D1130862C8DCD"
CERT_PATH = None  # Use 'cert.pem' if you want to verify SSL with a custom cert


def send_notification(title: str, message: str, user_ids: List[str], url: str = "", using_auth: bool = True) -> requests.Response:

    headers = {
        'Gateway-key': GATEWAY_KEY,
        'Content-Type': 'application/json',
        'Cookie': COOKIE_SESSION
    }

    payload = {
        "title": title,
        "message": message,
        "url": url,
        "using_auth": using_auth,
        "user_ids": user_ids
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            data=json.dumps(payload),
            verify=CERT_PATH if CERT_PATH else False
        )
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Error sending notification: {e}")
        raise
    

# === Example Usage ===
if __name__ == "__main__":
    response = send_notification(
        title="ขอใช้งานกระเป๋ายาฉุกเฉิน",
        message="น.อ.พงค์เทพ จันทน์เสนะ (ศซว.ทอ.) ใช้งานทดสอบร่างกาย ศซว.ทอ. วันที่ 16-17 ก.ค.68 โดยขอรับวันที่ 15 ก.ค.68 (บ่าย)",
        user_ids=["pongthep", "mutita_ch", "neranut_s"]
    )
    print(response.status_code)
    print(response.text)
