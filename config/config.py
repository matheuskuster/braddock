import sys


def getFrameFromCamera(camera):
    _, frame = camera.read()
    return frame


def printMessage(msg, kind=''):
    if kind == 'w':
        print('[WARNING]', msg)
    elif kind == 'e':
        print('[ERROR]', msg)
    elif kind == 's':
        print('[SUCCESS]', msg)
    else:
        print(msg)


def setArguments(args):
    verboseMode = False
    onlyBallMode = False
    onlyLineMode = False
    fullMode = True

    args.pop(0)

    if '-v' in args:
        verboseMode = True
    if '-B' in args and '-L' in args:
        print('[ERROR] You can only set Line Mode or Ball Mode, not both')
        sys.exit(0)
    elif '-B' in args:
        onlyBallMode = True
        fullMode = False
    elif '-V' in args:
        onlyLineMode = True
        fullMode = False

    return verboseMode, onlyBallMode, onlyLineMode, fullMode
