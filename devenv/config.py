import os
import subprocess


def find_confg(path):
    pass


class Repo(dict):
    def checkout(self, dest):
        cmd = ['git', 'clone', self['git'], dest]
        proc = subprocess.Popen(cmd)
        proc.wait()


class Config(dict):
    def __init__(self, data):
        self.update(data)

    def repos(self):
        pass

    def ensure_checkout(self, path):
        if len(self['repos']) == 1:
            # single repo project
            repo_data = list(self['repos'].values())[0]
            Repo(repo_data).checkout(path)
        else:
            # mutlie repo project
            repo_path = os.path.join(path, 'src')
            os.makedirs(repo_path)
            for repo in repos.values():
                Rep(repo_data).checkout(repo_data)
