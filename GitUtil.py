import requests
import json
import subprocess
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
            # subprocess.check_call(['git', 'fetch', '--all'], shell=True, cwd=self.PROJECT_PATH)
            # subprocess.check_call(['git', 'reset', '--hard', 'origin'], shell=True, cwd=self.PROJECT_PATH)
            # subprocess.check_call(['git', 'pull'], shell=True, cwd=self.PROJECT_PATH)
            subprocess.check_call(['cd', self.PROJECT_PATH, '&&', 'git', 'fetch', '--all'], shell=True)
            subprocess.check_call(['cd', self.PROJECT_PATH, '&&', 'git', 'reset', '--hard', 'origin'], shell=True)
            subprocess.check_call(['cd', self.PROJECT_PATH, '&&', 'git', 'pull'], shell=True)

            return

        print 'Start cloning ' + self.user + '/' + self.repo
        # sshUrl = 'git@github.com:'+self.user+'/'+self.repo+'.git'
        httpsUrl = 'https://github.com/'+self.user+'/'+self.repo+'.git'
        # subprocess.check_call(['git', 'clone', httpsUrl], shell=True, cwd=Commons.REPO_PATH)
        subprocess.check_call(['git', 'clone', httpsUrl, self.PROJECT_PATH], shell=True)

    def resetVersion(self, sha):
        # subprocess.check_call(['git', 'reset', '--hard', sha], shell=True, cwd=self.PROJECT_PATH)
        # subprocess.check_call(['git', 'clean', '-xdf'], shell=True, cwd=self.PROJECT_PATH)
        subprocess.check_call(['cd', self.PROJECT_PATH, '&&', 'git', 'reset', '--hard', sha], shell=True)
        subprocess.check_call(['cd', self.PROJECT_PATH, '&&', 'git', 'clean', '-xdf'], shell=True)

    def mvnInstall(self):
        try:
            # subprocess.check_call(['mvn', 'clean', 'install', '-DskipTests'], shell=True, cwd=self.PROJECT_PATH)
            # subprocess.check_call(['mvn', 'clean', 'install', '-Dmaven.test.skip=true'], shell=True, cwd=self.PROJECT_PATH)
            subprocess.check_call(['cd', self.PROJECT_PATH, '&&', 'mvn', 'clean', 'install', '-Dmaven.test.skip=true'], shell=True)
        except:
            pass
