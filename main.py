import sys
import cv2
import numpy as np
from config import *


def getFrameFromCamera(camera):
    ret, frame = camera.read()
    return frame


def main():
    verboseMode, onlyBallMode, onlyLineMode = setArguments(sys.argv)

    camera = cv2.VideoCapture(0)

    while True:
        frame = getFrameFromCamera(camera)

        if verboseMode:
            cv2.imshow('Webcam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
