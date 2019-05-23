import sys
import cv2
import numpy as np
from config import *


def getFrameFromCamera(camera):
    _, frame = camera.read()
    return frame


def handleRepetedLists(repetedRadius, repetedX, repetedY, x, y, r):
    if len(repetedRadius) < 3 and len(repetedX) < 3 and len(repetedY) < 3:
        repetedRadius.append(r)
        repetedX.append(x)
        repetedY.append(y)

    else:
        repetedRadius.pop(-1)
        repetedRadius.insert(0, r)

        repetedX.pop(-1)
        repetedX.insert(0, x)

        repetedY.pop(-1)
        repetedY.insert(0, y)


def calculateMedium(repetedRadius, repetedX, repetedY):
    if len(repetedRadius) == len(repetedX) and len(repetedX) == len(repetedY):
        divider = len(repetedX)

        mediumX = ((sum(repetedX)) // divider)
        mediumY = ((sum(repetedY)) // divider)
        mediumRadius = ((sum(repetedRadius)) // divider)

        return mediumX, mediumY, mediumRadius

    return None, None, None


def main():

    repetedRadius, repetedX, repetedY = [], [], []
    mediumX, mediumY, mediumRadius = None, None, None

    verboseMode, onlyBallMode, onlyLineMode = setArguments(sys.argv)
    camera = cv2.VideoCapture(0)

    elementForTopHat = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (5, 5))

    elementForDilate = cv2.getStructuringElement(
        cv2.MORPH_CROSS, (1, 1)
    )

    kernel = np.ones((3, 3), np.uint8)

    while True:

        image = getFrameFromCamera(camera)
        output = image.copy()
        blur = cv2.medianBlur(image, 5)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(blur, 80, 100, apertureSize=3)
        processedImage = gray * canny

        morphology = cv2.morphologyEx(
            processedImage, cv2.MORPH_TOPHAT, elementForTopHat)

        treatedImage = cv2.add(morphology, morphology)

        # cv2.imshow('treated', treatedImage)

        # detect circles in the image
        circles = cv2.HoughCircles(
            treatedImage, cv2.HOUGH_GRADIENT, dp=1, param1=1, param2=62, minDist=500)

        # ensure at least some circles were found
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            (x, y, r) = circles[0]
            # print('Raio:', r)
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            handleRepetedLists(repetedRadius, repetedX, repetedY, x, y, r)

            mediumX, mediumY, mediumRadius = calculateMedium(
                repetedRadius, repetedX, repetedY)

        if mediumRadius != None and mediumX != None and mediumY != None:
            cv2.circle(output, (mediumX, mediumY),
                       mediumRadius, (0, 255, 0), 4)
            cv2.rectangle(output, (mediumX - 5, mediumY - 5),
                          (mediumX + 5, mediumY + 5), (0, 128, 255), -1)

        # show the output image
        cv2.imshow("output", np.hstack([image, output]))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
