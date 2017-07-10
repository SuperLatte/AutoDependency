import requests
import json
from subprocess import call
import Commons
import os

class GitUtil():

    def __init__(self, user, repo):
        self.user = user
        self.repo = repo
        self.PROJECT_PATH = Commons.REPO_PATH+self.repo+'/'
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
        if str(response.status_code) == '404':
            return []
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
            print 'Start pulling ' + self.user + '/' + self.repo

            call('git fetch --all', cwd=self.PROJECT_PATH, shell=True)
            call('git reset --hard origin', cwd=self.PROJECT_PATH, shell=True)
            call('git pull', cwd=self.PROJECT_PATH, shell=True)

            return

        print 'Start cloning ' + self.user + '/' + self.repo
        # sshUrl = 'git@github.com:'+self.user+'/'+self.repo+'.git'
        httpsUrl = 'https://github.com/'+self.user+'/'+self.repo+'.git'

        call('git clone '+httpsUrl+' '+self.PROJECT_PATH, shell=True)


    def resetVersion(self, sha):
        print 'Start reset version'

        call('git reset --hard '+sha, cwd=self.PROJECT_PATH, shell=True)
        call('git clean -xdf', cwd=self.PROJECT_PATH, shell=True)

    def mvnInstall(self):
        print 'Maven install'
        try:
            # subprocess.check_call(['mvn', 'clean', 'install', '-DskipTests'], shell=True, cwd=self.PROJECT_PATH)

            call('mvn clean install -Dmaven.test.skip=true', cwd=self.PROJECT_PATH, shell=True)
        except:
            pass
