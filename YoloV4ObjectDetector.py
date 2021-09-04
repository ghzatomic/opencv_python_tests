import numpy as np 
import cv2
import time
import os

yolo_path = "yolo/yolov4optimal"

labelsPath = os.path.sep.join([yolo_path, "coco.names"])
weightsPath = os.path.sep.join([yolo_path, "yolov4.weights"])
configPath = os.path.sep.join([yolo_path, "yolov4.cfg"])

class ObjectDetector:

    def __init__(self):
        self.confidence_thresold = 0.5
        self.thresold = 0.3
        self.LABELS = open(labelsPath).read().strip().split("\n")
        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3),
            dtype="uint8")
        self.use_cuda = True
        self.net = cv2.dnn_DetectionModel(configPath, weightsPath)
        self.net.setInputSize(416, 416)
        self.net.setInputScale(1.0/255.0)
        self.net.setInputSwapRB(True)
        if self.use_cuda:
            #self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV) 
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        
    @staticmethod
    def createImageFromPath(imagePath):
        return cv2.imread(imagePath)

    def detectaImagem(self, imagePath, show=False):
        image = ObjectDetector.createImageFromPath(imagePath)
        image = self.detectaImagemCV2(image)
        if show:
            cv2.imshow("Image", image)
            cv2.waitKey(0)

            cv2.destroyAllWindows()
            
        return image

    def detectaImagemCV2(self, image):
        print("Detectando ... ")
        (H, W) = image.shape[:2]

        image_center = (int(W/2) , int(H/2))
        color_image_center = (0, 255, 0)
        cv2.circle(image, image_center, 5, color_image_center, 2)
        classes, confidences, boxes = self.net.detect(image, confThreshold=self.confidence_thresold, nmsThreshold=self.thresold)

        for classID, confidence, box in zip(classes.flatten(), confidences.flatten(), boxes):
            if confidence > self.confidence_thresold:
                color = (255, 0, 0)
                
                (x, y) = (box[0], box[1])
                (w, h) = (box[2], box[3])
                
                center_coordinates_detected = (int(x+w/2),int(y+h/2))
            
                diff_X = image_center[0] - center_coordinates_detected[0]
                diff_Y = image_center[1] - center_coordinates_detected[1]
                
                cv2.circle(image, center_coordinates_detected, 5, (255,255,0), 2)
                
                cv2.circle(image, center_coordinates_detected, 5, color_image_center, 2)
                cv2.rectangle(image, box, color_image_center, 1)
                text = "{}: {:.4f}".format(self.LABELS[classID], confidence)
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 2)
                
        return image

    