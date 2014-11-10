import json
import os
import zipfile


class Libraryfunctions(object):
    """docstring for Libraryfunctions"""
    def __init__(self):
        super(Libraryfunctions, self).__init__()
        self.ProjectFolder = os.path.join('app/Projects')
        self.StaticFolder = os.path.join('app/static')
        self.ProjectFolderPath = os.path.join(os.getcwd(), self.ProjectFolder)
        self.StaticFolderPath = os.path.join(os.getcwd(), self.StaticFolder)

    def CheckOut(self, project):
        #Is used for checking out projects
        j = self.ReadProjectDict(project)
        j['CheckedOut'] = True
        self.WriteProjectDict(project, j)

    def InitProject(self, project):
        #Is used for initializing projects
        InitDict = {'CheckedOut': False}
        self.WriteProjectDict(project, InitDict)

    def WriteProjectDict(self, project, data):
        #A base class that is used to write json files for projects
        if project not in os.listdir(self.ProjectFolderPath):
            os.mkdir('{}/'.format(
                os.path.join(self.ProjectFolderPath, project))
            )
        with open(
                '{}/.lir'.format(
                    os.path.join(self.ProjectFolderPath, project)), 'w+') as f:
            f.write(json.dumps(data, sort_keys=True, indent=4))

    def ReadProjectDict(self, project):
        #A base class that is used to read json files for projects
        with open(
                '{}/.lir'.format(os.path.join(
                    self.ProjectFolderPath, project)), 'r') as f:
            f = f.read()
        j = json.loads(f)
        j = dict(j)
        return j

    def CheckIn(self, project):
        #Is used for checking in projects
        j = self.ReadProjectDict(project)
        j['CheckedOut'] = False
        self.WriteProjectDict(project, j)

    def ZipProject(self, project):
        #This is a function for recursively zip a folder
        with zipfile.ZipFile('{}.zip'.format(
                os.path.join(
                    self.StaticFolderPath, project
                    )), 'w', zipfile.ZIP_DEFLATED) as zipf:
            for base, dirs, files in os.walk(
                    os.path.join(
                        self.ProjectFolderPath.replace(os.getcwd() + '/', ''),
                        project)):
                for file in files:
                    zipf.write(os.path.join(base, file))

    def UnZipProject(self, project):
        pass

    def DeleteProject(self, project):
        os.popen('rm {} -r'.format(os.path.join(
            self.ProjectFolderPath, project)))

if __name__ == '__main__':
    #Do nothing when this is imported
    pass
