import requests
import subprocess


class Github:
    def __init__(self, token):
        self.r = requests.Session()
        self.__token = token
        self.r.headers['Authorization'] = "token" + " " + token
        self.r.headers['Content-Type'] = 'application/json'
        self.r.headers['accept'] = "application/vnd.github.v3+json"

    @property
    def git_directory(self):
        return subprocess.check_output("git remote get-url origin").decode('utf-8')

    def create_issue(self, data: dict):
        raw_url = self.git_directory.split('/')
        url = raw_url[3] + "/" + raw_url[4].split('.')[0]
        self.r.post(f"https://api.github.com/repos/{url}/issues", json=data)

    def get_token(self):
        return self.__token
