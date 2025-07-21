import subprocess
import shlex
import shutil
from pathlib import Path
from sys import platform
from exception import PlatformException
from typing import Union
import time
import json
import os
import time
from typing import Optional
from typing import Final


TOKEN_FILE:Final[str] = "token.json"
TOKEN_LIFETIME:Final[int] = 3600

def check_git_installation(command:str="git --exec-path", timeout:float=1.0) -> bool:
    result = None
    argument = shlex.split(s=command)
    with subprocess.Popen(args=argument, stdout=subprocess.PIPE) as proc:
        output, _ = proc.communicate(timeout=timeout)
        result = output.decode('utf-8','ignore')
    return result is not None


def check_installation_v2():
    return shutil.which("git") is not None


def get_uipath_command_exec() -> Union[str, None]:
    default_path = "AppData/Local/Programs/UiPath/Studio"
    if platform != "win32":
        raise PlatformException
    
    uipath_command_path = Path.home() / default_path
    if not Path.exists(uipath_command_path):
        return None
    return uipath_command_path / 'UiPath.Studio.CommandLine.exe'

def is_valid_url(url:str):
    import re
    regex = re.compile(
        r'^https?://' 
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|' 
        r'localhost|' 
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)


class TokenManager:
    def __init__(self, token_file: str = TOKEN_FILE, lifetime: int = TOKEN_LIFETIME):
        self.token_file = token_file
        self.token_lifetime = lifetime  

    def save_token(self, token_value: str) -> None:
        data = {
            "token": token_value,
            "created_at": int(time.time()) 
        }
        with open(self.token_file, "w") as f:
            json.dump(data, f)

    def load_token(self) -> Optional[str]:
        if not os.path.exists(self.token_file):
            return None
        try:
            with open(self.token_file, "r") as f:
                data = json.load(f)
            return data.get("token")
        except (json.JSONDecodeError, FileNotFoundError, KeyError):
            return None

    def is_token_expired(self) -> bool:
        if not os.path.exists(self.token_file):
            return True
        try:
            with open(self.token_file, "r") as f:
                data = json.load(f)
            created_at = data.get("created_at", 0)
            return (int(time.time()) - created_at) > self.token_lifetime
        except (json.JSONDecodeError, FileNotFoundError, KeyError):
            return True

    def get_token(self) -> Optional[str]:
        if self.is_token_expired():
            return None
        return self.load_token()

    def delete_token(self) -> None:
        if os.path.exists(self.token_file):
            os.remove(self.token_file)
