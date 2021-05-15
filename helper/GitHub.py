import requests, json
from github import Github

config = json.load(open('config.json', 'r'))

class GitHub():
    path = "https://raw.githubusercontent.com/"
    username = str()
    repository = str()
    branch = str()
    GitHub_Client = None
    GitHub_Repo = None
  
    def __init__(self, username = 'mrm-36', repository = 'Algorithms', branch = 'main'):
        self.username, self.repository, self.branch = username, repository, branch
        self.path += username + "/" + repository + "/" + branch + "/"

    def get_file(self, filename):
        try:
            url = self.path + filename
            return requests.get(url).text
        except Exception: 
            return ""

    def add_file(self, filename, code):
        try:
            if self.GitHub_Client == None: self.GitHub_Client = Github(config['GitHub_Token'])
            if self.GitHub_Repo == None: 
                self.GitHub_Repo = self.GitHub_Client.get_repo(self.username + "/" + self.repository)

            self.GitHub_Repo.create_file(filename, "API Created " + filename, code, branch= self.branch)
            return True
        except Exception as ex:
            return ex
