from GitUtil import GitUtil
import Commons
import os
from subprocess import call
import json

def callGraph(user, repo, tag):
    OUTPUT_REPO_PATH = Commons.OUTPUT_PATH+repo+'/'
    if not os.path.exists(OUTPUT_REPO_PATH):
        os.mkdir(OUTPUT_REPO_PATH)

    # TARGET_PATH = Commons.REPO_PATH+repo+'/target/'
    # if not os.path.exists(TARGET_PATH):
    #     return

    OUTPUT_VERSION_PATH = OUTPUT_REPO_PATH+tag+'/'
    if not os.path.exists(OUTPUT_VERSION_PATH):
        os.mkdir(OUTPUT_VERSION_PATH)

    PROJECT_PATH = Commons.REPO_PATH+repo+'/'
    for root, dirs, files in os.walk(PROJECT_PATH):
        for file in files:
            if file.endswith('.jar') and 'target' in root:
                call('java -jar '+Commons.CALLTOOL_PATH+' '+root+'/'+file+' > '+OUTPUT_VERSION_PATH+file[:-4]+'.tmp', shell=True)

def generateGraph(user, repo):
    for root, dirs, files in os.walk(Commons.OUTPUT_PATH+repo+'/'):
        for file in files:
            if file.endswith('.tmp'):
                with open(root+'/'+file) as f:
                    callGraphs = f.readlines()
                callGraphs = [x.strip() for x in callGraphs]
                callGraphs = list(set(callGraphs))

                class_call = []
                method_call = []
                for call in callGraphs:
                    if call.startswith('C'):
                        if '$' in call:
                            continue
                        origin = call[2:].split(' ')[0]
                        call_obj = call[2:].split(' ')[1]
                        if (call_obj.startswith('[')):
                            continue
                        class_call.append({
                            "origin": origin,
                            "call": call_obj
                        })
                    elif call.startswith('M'):
                        origin = call[2:].split(' ')[0]
                        call_obj = call[2:].split(' ')[1][3:]
                        origin_class = origin.split(':')[0]
                        origin_method = origin.split(':')[1]
                        call_class = call_obj.split(':')[0]
                        call_method = call_obj.split(':')[1]
                        method_call.append({
                            "origin": {
                                "class": origin_class,
                                "method": origin_method
                            },
                            "call": {
                                "class": call_class,
                                "method": call_method
                            }
                        })
                callGraphs_output = {
                    'class_call': class_call,
                    'method_call': method_call
                }
                output_file = open(root+'/'+file[:-4]+'.json', 'wb')
                output_file.write(json.dumps(callGraphs_output))

                print file + ' done.'
    pass

if __name__ == "__main__":
    print "Program starts"

    if not os.path.exists(Commons.REPO_PATH):
        os.mkdir(Commons.REPO_PATH)

    if not os.path.exists(Commons.OUTPUT_PATH):
        os.mkdir(Commons.OUTPUT_PATH)

    with open("projects.json") as f:
        projects = f.readlines()

    projects = ''.join([x.strip() for x in projects])
    projects = json.loads(str(projects))

    for project in projects:
        user = project['user']
        repo = project['repo']

        gitUtil = GitUtil(user, repo)
        gitUtil.clone()

        tags = gitUtil.getTags()
        for tag in tags:
            name = tag['name']
            sha = tag['sha']

            gitUtil.resetVersion(sha)
            gitUtil.mvnInstall()
            callGraph(user, repo, name)

        generateGraph(user, repo)
    # callGraph('apache', 'maven-release', 'maven-release-2.5.3')

    print 'Program ends'