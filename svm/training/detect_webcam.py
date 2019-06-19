import sys
import dlib
import cv2

jumpFrames = 10
camera = cv2.VideoCapture(2)
framesCounter = 0
detector = dlib.simple_object_detector('./resources/detect_balls.svm')


def getRadius(left, top, right, bottom):
    radiusX = (right - left)//2
    radiusY = (bottom - top)//2
    mediumRadius = (radiusX + radiusY)//2

    return mediumRadius


while camera.isOpened():
    ret, frame = camera.read()
    detectedBalls = detector(frame, 1)
    for ball in detectedBalls:
        left, top, right, bottom = (int(ball.left()), int(
            ball.top()), int(ball.right()), int(ball.bottom()))

        # cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 3)

        radius = getRadius(left, top, right, bottom)
        centerX = left + radius
        centerY = top + radius
        cv2.rectangle(frame, (centerX - 2, centerY - 2),
                      (centerX + 2, centerY + 2), (255, 0, 0), 2)

        cv2.circle(frame, (centerX, centerY), radius, (0, 255, 0), 2)

        cv2.line(frame, (centerX, centerY),
                 (centerX + radius, centerY), (255, 0, 0), 1)

    cv2.imshow('Ball detection', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

camera.release()
cv2.destroyAllWindows()
sys.exit(0)
