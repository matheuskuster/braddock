import dlib

options = dlib.simple_object_detector_training_options()
options.add_left_right_image_flips = True
options.C = 5

detector = dlib.train_simple_object_detector(
    './resources/training_balls.xml', './resources/detect_balls.svm', options)
