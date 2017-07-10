import os

global PROJECT_PATH
global REPO_PATH

# PROJECT_PATH = 'D:/Repository/PycharmProjects/AutoDependency/'
PROJECT_PATH = os.getcwd() + '/'

REPO_PATH = PROJECT_PATH + 'repos/'
TOOL_PATH = PROJECT_PATH + 'tools/'
CALLTOOL_PATH = TOOL_PATH + 'JavaCallGraph.jar'

OUTPUT_PATH = PROJECT_PATH + 'output/'

