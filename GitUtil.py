import requests
import json
import subprocess
import Commons
import os

class GitUtil():

    def __init__(self, user, repo):
        self.user = user
        self.repo = repo
        self.PROJECT_PATH = Commons.REPO_PATH+self.repo+'\\'
        pass

    def getTags(self):
        session = requests.session()
        session.headers.update(
            {
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
            }
        )
        response = session.get('https://api.github.com/repos/'+self.user+'/'+self.repo+'/git/refs/tags')
        # print json.dumps(response.json())
        tags = response.json()
        result = []
        for tag in tags:
            tag_name = tag['url'].split('/')[-1]
            tag_sha = tag['object']['sha']
            result.append({
                'name': tag_name,
                'sha': tag_sha
            })

        return result


    def clone(self):


        if os.path.exists(self.PROJECT_PATH):
            print 'Start pulling ' + self.user + '\\' + self.repo
            subprocess.check_call(['git', 'fetch', '--all'], shell=True, cwd=self.PROJECT_PATH)
            subprocess.check_call(['git', 'reset', '--hard', 'origin/master'], shell=True, cwd=self.PROJECT_PATH)
            subprocess.check_call(['git', 'pull'], shell=True, cwd=self.PROJECT_PATH)
            return

        print 'Start cloning ' + self.user + '\\' + self.repo
        sshUrl = 'git@github.com:'+self.user+'/'+self.repo+'.git'
        subprocess.check_call(['git', 'clone', sshUrl], shell=True, cwd=Commons.REPO_PATH)

    def resetVersion(self, sha):
        subprocess.check_call(['git', 'reset', '--hard', sha], shell=True, cwd=self.PROJECT_PATH)
        subprocess.check_call(['git', 'clean', '-xdf', sha], shell=True, cwd=self.PROJECT_PATH)

    def mvnInstall(self):
        try:
            # subprocess.check_call(['mvn', 'clean', 'install', '-DskipTests'], shell=True, cwd=self.PROJECT_PATH)
            subprocess.check_call(['mvn', 'clean', 'install', '-Dmaven.test.skip=true'], shell=True, cwd=self.PROJECT_PATH)
        except:
            pass
