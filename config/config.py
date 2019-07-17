import sys
import serial

PORT, SPEED = '/dev/ttyACM0', 9600

arduinoSerial = serial.Serial(PORT, SPEED)


def getFrameFromCamera(camera):
    _, frame = camera.read()
    return frame


def sendToArduino(msg):
    print('Sending [{}] to Arduino...'.format(msg))
    arduinoSerial.write(msg.encode())


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
        printMessage('You can only set Line Mode or Ball Mode, not both', 'e')
        sys.exit(0)
    elif '-B' in args:
        onlyBallMode = True
        fullMode = False
    elif '-L' in args:
        onlyLineMode = True
        fullMode = False

    return verboseMode, onlyBallMode, onlyLineMode, fullMode
