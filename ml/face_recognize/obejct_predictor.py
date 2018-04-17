# -*- encoding:utf-8 -*-

import os,sys,glob
import dlib
from skimage import io

class ObjectPredictor:
    def __init__(self,**kwargs):
        options = dlib.shape_predictor_training_options()
        data = kwargs
        options.oversampling_amount = get_value("oversampling_amount",kwargs,300)
        options.nu = get_value("nu",kwargs,0.05)
        options.tree_depth = get_value("tree_depth",kwargs,3)
        options.be_verbose = get_value("be_verbose",kwargs,True)
        self.options = options
        self.predictor = None

    def recover_model_from_file(self,predictor_path):
        self.predictor = dlib.shape_predictor(predictor_path)

    def save_model_to_file(self,predictor_path):
        self.predictor.save(predictor_path)

    def train_from_file(self, data_path, predictor_path):
        training_xml_path = os.path.join(data_path, "training.xml")
        dlib.train_shape_predictor(training_xml_path, predictor_path, self.options)
        self.detector = dlib.simple_object_detector(predictor_path)

    def test_from_file(self,testing_xml_path,predictor_path):
        dlib.test_shape_predictor(testing_xml_path, predictor_path)


    def train(self, images, full_object_detection):
        self.detector = dlib.train_simple_object_detector(images, full_object_detection, self.options)

    def test(self, images, full_object_detection):
        result = dlib.test_simple_object_detector(images, full_object_detection, self.predictor)
        return result

    def predict(self,img):
        result = []
        dets = self.predictor(img, det)
        return result

    def get_value(key,data,value):
        try:
            value = data[key]
        except:
            value = value
        return value

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Give the path to the examples/faces directory as the argument to this "
            "program. For example, if you are in the python_examples folder then "
            "execute this program by running:\n"
            "    ./train_shape_predictor.py ../examples/faces")
        exit()
    faces_folder = sys.argv[1]

    options = dlib.shape_predictor_training_options()
    options.oversampling_amount = 300
    options.nu = 0.05
    options.tree_depth = 2
    options.be_verbose = True

    training_xml_path = os.path.join(faces_folder, "training_with_face_landmarks.xml")
    dlib.train_shape_predictor(training_xml_path, "predictor.dat", options)

    print("\nTraining accuracy: {}".format(
        dlib.test_shape_predictor(training_xml_path, "predictor.dat")))

    testing_xml_path = os.path.join(faces_folder, "testing_with_face_landmarks.xml")
    print("Testing accuracy: {}".format(
        dlib.test_shape_predictor(testing_xml_path, "predictor.dat")))

    predictor = dlib.shape_predictor("predictor.dat")
    detector = dlib.get_frontal_face_detector()

    print("Showing detections and predictions on the images in the faces folder...")
    win = dlib.image_window()
    for f in glob.glob(os.path.join(faces_folder, "*.jpg")):
        print("Processing file: {}".format(f))
        img = io.imread(f)

        win.clear_overlay()
        win.set_image(img)
        dets = detector(img, 1)
        print("Number of faces detected: {}".format(len(dets)))
        for k, d in enumerate(dets):
            print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                k, d.left(), d.top(), d.right(), d.bottom()))
            # Get the landmarks/parts for the face in box d.
            shape = predictor(img, d)
            print("Part 0: {}, Part 1: {} ...".format(shape.part(0),
                                                    shape.part(1)))
            # Draw the face landmarks on the screen.
            win.add_overlay(shape)

        win.add_overlay(dets)
        dlib.hit_enter_to_continue()