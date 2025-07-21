import os
import requests
import os
from utils import TokenManager

FOLDER_API_URL = "https://dceyy2lx.adam.adroot.edf.fr/odata/Folders"

token_manager = TokenManager()

def login() -> None:
    payload = {
        "tenancyName": os.environ.get("TENANCYNAME"),
        "usernameOrEmailAddress": os.environ.get("USERNAMEOREMAILADDRESS"),
        "password": os.environ.get("PASSWORD")
    }
    try:
        response = requests.post(
            os.environ.get("AUTH_URL"), 
            json=payload, 
            headers={'Content-Type': 'application/json'}, 
            timeout=1,
            verify=False
        )
        result = response.json()
        token_manager.save_token(result.get('result'))
    except requests.exceptions.RequestException as e:
        raise e.strerror


def get_folder():
    jwt_token = token_manager.get_token()
    if jwt_token is None:
        login()
        jwt_token = token_manager.get_token()
    try:
        result = requests.get(url=FOLDER_API_URL, timeout=1, verify=False, headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {jwt_token}'
        })
        result = result.json()
    except requests.exceptions.RequestException as exc:
        return None
    return result
    
    

if __name__ == '__main__':
    print(get_folder())
