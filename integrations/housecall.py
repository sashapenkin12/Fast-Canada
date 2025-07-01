import requests
from django.conf import settings


def send_to_housecall_pro(contact):
    url = "https://api.housecallpro.com/v1/jobs"
    headers = {
        "Authorization": f"Bearer {settings.HOUSECALL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": contact.name,
        "phone": contact.phone,
        "email": contact.email,
        "address": contact.address,
        "description": contact.description
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
