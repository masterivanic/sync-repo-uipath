import subprocess
import shlex

from utils import get_uipath_command_exec
from utils import check_installation_v2
from utils import is_valid_url
from exception import GitNotFoundExeception
from exception import UiPathNotFoundExeception
from pathlib import Path
from typing import Union, Any
import json
import os
import sys
import os

""" 
    robot init (initialize git repository)
    robot deploy (this will commit and push to orchestor)
    robot deploy --dev: deploy and commit on dev branch
    robot deploy --prod: deploy and commit on main branch
    robot analyze
    robot repair 🤖 (feature)
"""
     
class RobotCommand:

    def __init__(self):
        self.uipath_commandline = get_uipath_command_exec()
        self.current_directory = Path.cwd()

        if check_installation_v2() is False:
            raise GitNotFoundExeception
        if self.uipath_commandline is None:
            raise UiPathNotFoundExeception

    
    def get_process_id_from_orchestrator(self, token:str):
        pass

    
    def get_project_info(self) -> dict[str, Any]:
        json_file_path = self.get_project_json_path()
        with open(file=json_file_path) as file:
            data = json.load(file)
            return dict(
                name=data["name"], 
                id=data["projectId"], 
                version=data["projectVersion"], 
                target=data["targetFramework"]
            )
        return dict()


    def init_repository(self):
        is_git = self._is_git_project()
        if is_git is False:
            try:
                subprocess.run(['git', 'init'], check=True, capture_output=True)
                subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
                subprocess.run(['git', 'commit', '-m', 'init'], check=True)
                subprocess.run(['git', 'branch', '-M', 'main'], check=True)
                print("One step remaining 😊 to init your project", end="\n")
                origin_url = input("Enter origin url: ")
                if origin_url is None:
                    print("No remote repository add")
                else:
                    if is_valid_url(origin_url):
                        subprocess.run(['git', 'remote', 'add', 'origin', origin_url], check=True)
                        print("Initialized Git repository and remote origin add successfully... 🚀")
                    else:
                        print("Origin url entered is not a valid url")
            except subprocess.CalledProcessError as e:
                print("Failed to initialize repository:", e)
                sys.exit(1)
        else:
            print("Project is already initialize")


    def _is_git_project(self) -> bool:
        list_folder = os.listdir(self.current_directory)
        for file in list_folder:
            if file == ".git":
                return True
        return False

    def get_project_json_path(self) -> Union[str, None]:
        if Path.exists(self.current_directory / "project.json"):
            return self.current_directory / "project.json"
        return None

        
    def push_and_commit(self, target_branch:str="dev", commit_message:str=None) -> Union[int, None]:
        returncode = 0
        commit = "git commit -m " + commit_message
        push = f"git push remote {target_branch} origin/{target_branch}"
        argument = shlex.split(s=f"{commit} ';' {push}")
        with subprocess.Popen(args=argument, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
            output, _ = proc.communicate()
            returncode = proc.poll()
        return returncode
    
    def push_to_orchestrator(self, notes:str=None, mode="orchestrator", local_path:str=None) -> Union[int, None]:
        """
        refer to https://docs.uipath.com/fr/studio/standalone/2023.4/user-guide/about-publishing-automation-projects
        """
        project_path = self.get_project_json_path()
        if project_path is None:
            raise Exception("project not found")
        
        command = f"{self.uipath_commandline} publish --project-path {project_path} OrchestratorTenant --notes {notes}"
        if mode != "orchestrator":
            command = "None"

        argument = shlex.split(s=command)
        with subprocess.Popen(args=argument, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
            output, _ = proc.communicate()
            returncode = proc.poll()
        return returncode
        

    def deploy(self, target="dev", commit_message=None) -> str:
        if self._is_git_project():
            raise Exception("git project is not initialized")
        
        commit = self.push_and_commit(target_branch=target, commit_message=commit_message)
        push = None
        if commit is not None:
            self.push_to_orchestrator(notes=commit_message)
         
        if push is not None:
            return "process successfully deploy🚀"
        return "Error occur while deploying"

        


if __name__ == '__main__':
    #print(RobotCommand().get_package_id())
    pass
