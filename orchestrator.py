import os
import requests
import os
from utils import TokenManager
from typing import Union

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


def get_folder(folder_name:str = "DEVELOPPEMENT") -> Union[dict, None]:
    jwt_token = token_manager.get_token()
    if jwt_token is None:
        login()
        jwt_token = token_manager.get_token()
    try:
        result = requests.get(url=FOLDER_API_URL, timeout=1, verify=False, headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {jwt_token}'
        })
        result = result.json().get('value', []) # list of dict
        result = list(filter(lambda d:d['FullyQualifiedName'] == f'SIMA/{folder_name}', result))
        if len(result) == 1:
            return result[0]
    except requests.exceptions.RequestException as exc:
        return None
    return {}
    
    
if __name__ == '__main__':
    print(get_folder())
