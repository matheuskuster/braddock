import sys

def setArguments(args):
    verboseMode = False
    onlyBallMode = False
    onlyLineMode = False

    args.pop(0)

    if '-v' in args:
        verboseMode = True

    if '-B' in args and '-L' in args:
        print('[ERROR] You can only set Line Mode or Ball Mode, not both')
        sys.exit(0)
    elif '-B' in args:
        onlyBallMode = True
    elif '-V' in args:
        onlyLineMode = True

    return verboseMode, onlyBallMode, onlyLineMode
