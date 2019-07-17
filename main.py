import sys

import cv2
import dlib
import numpy as np

from config.ball import *
from config.config import *
from time import sleep


def calculateError(matriz):
    if not matriz[0] and not matriz[1] and not matriz[2] and not matriz[3] and matriz[4]:
        return '4'
    elif not matriz[0] and not matriz[1] and not matriz[2] and matriz[3] and matriz[4]:
        return '3'
    elif not matriz[0] and not matriz[1] and not matriz[2] and matriz[3] and not matriz[4]:
        return '2'
    elif not matriz[0] and not matriz[1] and matriz[2] and matriz[3] and not matriz[4]:
        return '1'
    elif not matriz[0] and not matriz[1] and matriz[2] and not matriz[3] and not matriz[4]:
        return '0'
    elif not matriz[0] and matriz[1] and matriz[2] and not matriz[3] and not matriz[4]:
        return '5'
    elif not matriz[0] and matriz[1] and not matriz[2] and not matriz[3] and not matriz[4]:
        return '6'
    elif matriz[0] and matriz[1] and not matriz[2] and not matriz[3] and not matriz[4]:
        return '7'
    elif matriz[0] and not matriz[1] and not matriz[2] and not matriz[3] and not matriz[4]:
        return '8'


def calculateDirection(x):
    listToSend = []
    errorMargin = 2

    listToSend.append(x < (32 + errorMargin))
    listToSend.append(x > (32 - errorMargin) and x < (64 + errorMargin))
    listToSend.append(x > (64 - errorMargin) and x < (96 + errorMargin))
    listToSend.append(x > (96 - errorMargin) and x < (128 + errorMargin))
    listToSend.append(x > (128 - errorMargin))

    return listToSend


def main():
    verboseMode, onlyBallMode, onlyLineMode, fullMode = setArguments(sys.argv)

    ballDetector = dlib.simple_object_detector('./resources/detect_balls.svm')

    message = ''
    lastMessage = 'F'

    frameCounter = 0
    maxFrames = 1

    camera = cv2.VideoCapture(2)
    camera.set(3, 320)
    camera.set(4, 240)

    if not camera.isOpened():
        printMessage('Impossible to use camera, it appears to be off', 'e')
        sys.exit(0)

    sleep(1)
    sendToArduino(lastMessage)
    while onlyLineMode or fullMode:
        frame = getFrameFromCamera(camera)
        cropFrame = frame[0:120, 0:160]
        gray = cv2.cvtColor(cropFrame, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh1 = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

        mask = cv2.erode(thresh1, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        _, contours, hierarchy = cv2.findContours(
            mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)

            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            direction = calculateDirection(cx)
            message = calculateError(direction)

            if verboseMode:
                cv2.line(cropFrame, (cx, 0), (cx, 720), (255, 0, 0), 1)

                cv2.line(cropFrame, (0, cy), (1280, cy), (255, 0, 0), 1)
                cv2.drawContours(cropFrame, contours, -1, (0, 255, 0), 1)

        if message != lastMessage:
            lastMessage = message
            sendToArduino(lastMessage)

        if verboseMode:
            cv2.imshow('Line', cropFrame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                sendToArduino('S')
                break

    cv2.destroyAllWindows()

    while onlyBallMode or fullMode:
        frame = getFrameFromCamera(camera)
        frameCounter += 1

        if frameCounter % maxFrames == 0:
            detectedBalls = ballDetector(frame, 1)

            if len(detectedBalls) == 0:
                message = 'D'

            else:
                for ball in detectedBalls:
                    left, top, right, bottom = (int(ball.left()), int(
                        ball.top()), int(ball.right()), int(ball.bottom()))

                    radius = getRadius(left, top, right, bottom)
                    centerX = left + radius
                    centerY = top + radius

                    message = calculateDirection(centerX)

                    if verboseMode:
                        cv2.rectangle(frame, (centerX - 2, centerY - 2),
                                      (centerX + 2, centerY + 2), (255, 0, 0), 2)

                        cv2.circle(frame, (centerX, centerY),
                                   radius, (0, 255, 0), 2)

                        cv2.line(frame, (centerX, centerY),
                                 (centerX + radius, centerY), (255, 0, 0), 1)

            if verboseMode:
                cv2.imshow('Ball detection', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    sendToArduino('P')
                    break

        if message != lastMessage:
            sendToArduino(lastMessage)
            lastMessage = message

    camera.release()
    cv2.destroyAllWindows()
    sys.exit(0)


if __name__ == '__main__':
    main()
