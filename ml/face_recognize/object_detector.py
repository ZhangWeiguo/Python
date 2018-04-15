import os,sys,glob,dlib
from skimage import io


class ObjectDetector:
    def __init__(self,**kwargs):
        options = dlib.simple_object_detector_training_options()
        try:
            add_left_right_image_flips = kwargs["add_left_right_image_flips"]
        except:
            add_left_right_image_flips = True
        try:
            C = kwargs["C"]
        except:
            C = 5
        try:
            num_threads = kwargs["num_threads"]
        except:
            num_threads = 4
        try:
            be_verbose = kwargs["be_verbose"]
        except:
            be_verbose = True        
        options.add_left_right_image_flips = add_left_right_image_flips
        options.C = C
        options.num_threads = num_threads
        options.be_verbose = be_verbose
        self.options = options

    def recover_model_from_file(self,detector_path):
        self.detector = dlib.simple_object_detector(detector_path)


    def train_from_file(self, data_path, detector_path):
        training_xml_path = os.path.join(data_path, "training.xml")
        testing_xml_path = os.path.join(data_path, "testing.xml")
        dlib.train_simple_object_detector(training_xml_path, detector_path, self.options)
        self.detector = dlib.simple_object_detector(detector_path)

    def test_from_file(self):
        dlib.test_simple_object_detector(training_xml_path, "detector.svm")

    def train_from_data(self):
        pass
    def test_from_data(self):
        pass

    def predict(self):
        dets = self.detector(img)
        return dets



