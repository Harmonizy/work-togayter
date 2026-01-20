import requests
import json
from typing import List

API_URL = "https://apigw.rtaf.mi.th/super-apps/v2/notifications/push-notification-to-app"
GATEWAY_KEY = "Bearer yAHSqMRdtaTeSlztcvW4820SxNbEITw5w_6NTT8LTu0GaeK7VHowcaj3gyXYK2H5k3znQAN93w2kc70vN-Hc0aw41v59edkG6i6C1H4Cl3CqnpJZFDVMKmIAfAdTZNnWu4xoFBvlkxME2G8VTXFMDTLR30ayreU_5sA2qn2xBBk540imq78QrZQdsMwnnmxlSsb8F42BufGgKTQX6npTHXCyqXjIrKmqQW8WCgtkexpTjHV6pVE3FhiSc0aoxyqR1yoir_3qUAg"
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
