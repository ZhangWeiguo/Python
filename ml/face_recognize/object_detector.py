# -*- encoding: utf-8 -*-
import os,sys,glob,dlib
from skimage import io


class ObjectDetector:
    def __init__(self,**kwargs):
        options = dlib.simple_object_detector_training_options()
        data = kwargs
        add_left_right_image_flips = get_value("add_left_right_image_flips",data,True)
        C = get_value("C",data,5)
        num_threads = get_value("num_threads",kwargs,4)
        be_verbose = get_value("be_verbose",kwargs,True)
        detection_window_size = get_value("detection_window_size",kwargs,6400)
        epsilon = get_value("epsilon",kwargs,0.01)
    
        options.add_left_right_image_flips = add_left_right_image_flips
        options.C = C
        options.num_threads = num_threads
        options.be_verbose = be_verbose
        options.detection_window_size = detection_window_size
        options.epsilon = epsilon
        self.options = options

    def recover_model_from_file(self,detector_path):
        self.detector = dlib.simple_object_detector(detector_path)

    def save_model_to_file(self,detector_path):
        self.detector.save(detector_path)

    def train_from_file(self, data_path, detector_path):
        '''
        In data_path
        training.xml and testing.xml must exists
        it must like this:
            <dataset>
            <name>Training faces</name>
            <comment>These are images from the PASCAL VOC 2011 dataset.</comment>
            <images>
            <image file='5.jpg'>
                <box top='0' left='0' width='448' height='300'/>
            </image>
            <image file='6.jpg'>
                <box top='0' left='0' width='593' height='300'/>
            </image>
            </images>
            </dataset>
        '''
        training_xml_path = os.path.join(data_path, "training.xml")
        testing_xml_path = os.path.join(data_path, "testing.xml")
        dlib.train_simple_object_detector(training_xml_path, detector_path, self.options)
        self.detector = dlib.simple_object_detector(detector_path)

    def test_from_file(self,testing_xml_path,detector_path):
        dlib.test_simple_object_detector(testing_xml_path, detector_path)


    def train(self, images, boxes):
        self.detector = dlib.train_simple_object_detector(images, boxes, self.options)

    def test(self, images, boxes):
        result = dlib.test_simple_object_detector(images, boxes, self.detector)
        precision = result.precision
        recall = result.recall
        return precision,recall

    def predict(self,img):
        result = []
        dets = self.detector(img)
        for det in dets:
            result.append(det)
        return result

    def get_value(key,data,value):
        try:
            value = data[key]
        except:
            value = value
        return value



if __name__ == "__main__":
    import os
    img_path = "D:\\Code\\Python\\ml\\face_recognize\\cars"
    path = [os.path.join(img_path,i) for i in os.listdir(img_path)]
    imgs = [io.imread(i) for i in path if i.endswith("jpg")]
    boxes = []
    for i in imgs:
        height,width,nums = i.shape
        r = dlib.rectangle(left=0,top=0,right=width,bottom=height)
        boxes.append([r])

    objectDetector = ObjectDetector()
    objectDetector.train(imgs,boxes)
    print objectDetector.test(imgs,boxes)