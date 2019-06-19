import os
import dlib
import cv2
import glob

print(dlib.test_simple_object_detector(
    './test_balls/test_answer.xml', './resources/detect_balls.svm'))

ballDetector = dlib.simple_object_detector('./resources/detect_balls.svm')

for image in glob.glob(os.path.join('test_balls', '*.jpg')):
    img = cv2.imread(image)

    detectedBalls = ballDetector(img)

    for ball in detectedBalls:
        left, top, right, bottom = (int(ball.left()), int(
            ball.top()), int(ball.right()), int(ball.bottom()))

        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)

    cv2.imshow('Ball detector', img)
    cv2.waitKey(0)

cv2.destroyAllWindows()
