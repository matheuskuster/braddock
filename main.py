import sys

import cv2
import dlib
import numpy as np

from config.ball import *
from config.config import *


def main():
    verboseMode, onlyBallMode, onlyLineMode, fullMode = setArguments(sys.argv)
    cameraPort = 0
    ballDetector = dlib.simple_object_detector('./resources/detect_balls.svm')

    camera = cv2.VideoCapture(cameraPort)
    if not camera.isOpened():
        printMessage('Impossible to use camera, it appears to be off', 'e')
        sys.exit(0)

    while onlyLineMode or fullMode:
        # Código de linha
        break

    while onlyBallMode or fullMode:
        frame = getFrameFromCamera(camera)
        detectedBalls = ballDetector(frame, 1)

        for ball in detectedBalls:
            left, top, right, bottom = (int(ball.left()), int(
                ball.top()), int(ball.right()), int(ball.bottom()))

            radius = getRadius(left, top, right, bottom)
            centerX = left + radius
            centerY = top + radius

            if verboseMode:
                cv2.rectangle(frame, (centerX - 2, centerY - 2),
                              (centerX + 2, centerY + 2), (255, 0, 0), 2)

                cv2.circle(frame, (centerX, centerY), radius, (0, 255, 0), 2)

                cv2.line(frame, (centerX, centerY),
                         (centerX + radius, centerY), (255, 0, 0), 1)

        if verboseMode:
            cv2.imshow('Ball detection', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    camera.release()
    cv2.destroyAllWindows()
    sys.exit(0)


if __name__ == '__main__':
    main()
