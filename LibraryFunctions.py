import json


def CheckOut(project):
    j = ReadProjectDict(project)
    j['CheckedOut'] = True
    WriteProjectDict(project, j)


def InitProject(project):
    InitDict = {'CheckedOut': False}
    WriteProjectDict(project, InitDict)


def WriteProjectDict(project, data):
    with open('Projects/{}/.lir'.format(project), 'w+') as f:
        f.write(json.dumps(data, sort_keys=True, indent=4))


def ReadProjectDict(project):
    with open('Projects/{}/.lir'.format(project), 'r') as f:
        f = f.read()
    j = json.loads(f)
    j = dict(j)
    return j


def CheckIn(project):
    j = ReadProjectDict(project)
    j['CheckedOut'] = False
    WriteProjectDict(project, j)


if __name__ == '__main__':
    pass
