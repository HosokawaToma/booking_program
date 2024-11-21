import requests
from .. import config
from .. import models
from .. import utilities

def validate_id_token(liff_id_token: str) -> models.LineUserInfo:
    url = "https://api.line.me/oauth2/v2.1/verify"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "id_token": liff_id_token,
        "client_id": config.LINE_CLIENT_ID()
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    
    return utilities.parse_line_user_info(response.json())