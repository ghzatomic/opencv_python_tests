import numpy as np 
import cv2
import time
import os
import math
from BluetoothArduinoCommunication import BluetoothArduinoCommunication

yolo_path = "yolo/yolov4optimal"

labelsPath = os.path.sep.join([yolo_path, "coco.names"])
weightsPath = os.path.sep.join([yolo_path, "yolov4.weights"])
configPath = os.path.sep.join([yolo_path, "yolov4.cfg"])


allowed_classes = ['person',"cat",
"dog",
"car;",
"bird",
"horse",
"bicycle",
"motorbike"]

class ObjectDetector(BluetoothArduinoCommunication):

    def __init__(self, connect_bt=False):
        BluetoothArduinoCommunication.__init__(self, connect=connect_bt)
        self.confidence_thresold = 0.4
        self.thresold = 0.2
        self.LABELS = open(labelsPath).read().strip().split("\n")
        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3),
            dtype="uint8")
        self.net = cv2.dnn_DetectionModel(configPath, weightsPath)
        self.net.setInputSize(416, 416)
        self.net.setInputScale(1.0/255.0)
        self.net.setInputSwapRB(True)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV) 
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        
    @staticmethod
    def createImageFromPath(imagePath):
        return cv2.imread(imagePath)

    def createLayers(self):
        if not self.ln:
            # determine only the *output* layer names that we need from YOLO
            self.ln = self.net.getLayerNames()
            self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        return self.ln


    def detectaImagem(self, imagePath, show=False):
        image = ObjectDetector.createImageFromPath(imagePath)
        image = self.detectaImagemCV2(image)
        if show:
            cv2.imshow("Image", image)
            cv2.waitKey(0)

            cv2.destroyAllWindows()
            
        return image

    def detectaImagemCV2(self, image):
        if not self.connected:
            self.do_connect()
        self.in_target = False
        (H, W) = image.shape[:2]
        image_center = (int(W/2) , int(H/2))
        color_image_center = (0, 255, 0)
        cv2.circle(image, image_center, 5, color_image_center, 2)
        start_time = time.time()
        classes, confidences, boxes = self.net.detect(image, confThreshold=self.confidence_thresold, nmsThreshold=self.thresold)
        #print("--- %s seconds ---" % (time.time() - start_time))
        if len(boxes) == 0:
            self.nao_encontrado()
        else:
            self.encontrado()
            detectados_arr = []
            for classID, confidence, box in zip(classes.flatten(), confidences.flatten(), boxes):
                if self.LABELS[classID] not in allowed_classes:
                    continue
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
                    detectados_arr.append([w*h,x,y,w,h,diff_X,diff_Y, box])
                    
            maior_enquadro = BluetoothArduinoCommunication.calcula_maior_quadrado(detectados_arr)
            if maior_enquadro and len(maior_enquadro)>0:
                self.determina_target(maior_enquadro[5], maior_enquadro[6])
                cv2.rectangle(image,maior_enquadro[7],(100,120,0),2)
            else:
                self.nao_encontrado()
        return image

    