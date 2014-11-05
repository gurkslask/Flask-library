import json
import os
import zipfile
ProjectFolder = os.path.join(os.getcwd(), 'Projects')

def CheckOut(project):
    #Is used for checking out projects
    j = ReadProjectDict(project)
    j['CheckedOut'] = True
    WriteProjectDict(project, j)


def InitProject(project):
    #Is used for initializing projects
    InitDict = {'CheckedOut': False}
    WriteProjectDict(project, InitDict)


def WriteProjectDict(project, data):
    #A base class that is used to write json files for projects
    if project not in os.listdir(ProjectFolder):
        os.mkdir('{}/'.format(os.path.join(ProjectFolder, project)))
    with open(
            '{}/.lir'.format(os.path.join(ProjectFolder, project)), 'w+') as f:
        f.write(json.dumps(data, sort_keys=True, indent=4))


def ReadProjectDict(project):
    #A base class that is used to read json files for projects
    with open(
            '{}/.lir'.format(os.path.join(ProjectFolder, project)), 'r') as f:
        f = f.read()
    j = json.loads(f)
    j = dict(j)
    return j


def CheckIn(project):
    #Is used for checking in projects
    j = ReadProjectDict(project)
    j['CheckedOut'] = False
    WriteProjectDict(project, j)


def ZipProject(project):
    with zipfile.ZipFile('{}.zip'.format(
            os.path.join(ProjectFolder, project)), 'w', zipfile.ZIP_DEFLATED) as zipf:
        for base, dirs, files in os.walk(
                os.path.join(ProjectFolder, project)):
            for file in files:
                zipf.write(os.path.join(base, file))


def UnZipProject(project):
    pass


if __name__ == '__main__':
    #Do nothing when this is imported
    pass
