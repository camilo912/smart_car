import cv2
import utils
import numpy as np
import tensorflow as tf
import dlib

class Decisor():
    def __init__(self):
        self.shape = (224, 320, 3)
        
        # model sess for being loaded just one time
        model_name  = "models/model_2.ckpt"
        self.sess = tf.Session()
        tf.saved_model.loader.load(self.sess, ['train'], model_name)
        
        detector_stop = dlib.fhog_object_detector('data/detector_stop.svm')
        detector_sem = dlib.fhog_object_detector('data/detector_sem.svm')
        self.detectors = [detector_stop, detector_sem]
        self.classes = ['stop', 'sem']
        
    
    def take_decision(self, img):
        detects = self.detect_objects(img)
        detects = [x for x in detects if x.distance < 25.0]

        if(len(detects)>0):
            return -1
        else:
            return self.predict(img)
    
    def predict(self, img):
        img = cv2.resize(img, (self.shape[1], self.shape[0]))
        outs = self.sess.run('output:0', feed_dict={'input:0':np.expand_dims(img, 0)})
        names = {j:i for i,j in utils.get_names().items()}

        return outs[0]

    def detect_objects(self, img):
        boxes, confidences, detector_idxs = dlib.fhog_object_detector.run_multiple(self.detectors, img, upsample_num_times=1, adjust_threshold=0.0)
        detects = []
        tmp = img.copy()

        for i,d in enumerate(boxes):
            dist = utils.distance(d.right()-d.left(), self.classes[detector_idxs[i]])
            # cv2.rectangle(tmp, (d.left(), d.top(), d.right()-d.left(), d.bottom()-d.top()), (0, 255, 0)) # just for debugging
            # cv2.putText(tmp,str(int(dist)),(d.left(), d.top()), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1,cv2.LINE_AA) # just for debugging
            detects.append(self.Detection(self.classes[detector_idxs[i]], dist))

        # if(len(boxes)>0): # just for debugging
        #     cv2.imshow('image', tmp) # just for debugging
        #     cv2.waitKey() # just for debugging

        return detects

    class Detection():
        def __init__(self, name, distance):
            self.name = name
            self.distance = distance