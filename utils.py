import subprocess
import shlex
import shutil
from pathlib import Path
from sys import platform
from exception import PlatformException
from typing import Union

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