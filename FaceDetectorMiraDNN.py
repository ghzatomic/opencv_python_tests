import numpy as np 
import cv2 as cv
import time
from time import sleep
from BluetoothArduinoCommunication import BluetoothArduinoCommunication

class FaceDetectorMira(BluetoothArduinoCommunication):

    def __init__(self, connect_bt=False):
        BluetoothArduinoCommunication.__init__(self)
        self.face_classifier = FaceDetectorMira.createCascadeClassifier_face()
        self.eye_classifier = FaceDetectorMira.createCascadeClassifier_olhos()
        self.connect = True

    def detectaFaceImagem(self, image):
        image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        faces = self.face_classifier.detectMultiScale(image_gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv.rectangle(image, (x,y), (x+w, y+h), (255,0,0), 2)
        return image

    def detectaFace2(self,img):
        if not self.connected:
            self.do_connect()
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (5, 5), 0)
        (H, W) = img.shape[:2]
        h, w = img.shape[:2]
        image_center = (int(W/2) , int(H/2))
        color_image_center = (0, 255, 0)
        start = time.time()
        modelFile = "models/res10_300x300_ssd_iter_140000.caffemodel"
        configFile = "models/deploy.prototxt.txt"
        net = cv.dnn.readNetFromCaffe(configFile, modelFile)
        blob = cv.dnn.blobFromImage(cv.resize(img, (300, 300)), 1.0,(300, 300), (104.0, 117.0, 123.0))
        net.setInput(blob)
        faces = net.forward()
        end = time.time()
        #print("[INFO] {:.6f} seconds".format(end - start))
        cv.circle(img, image_center, 5, color_image_center, 2)
        font                   = cv.FONT_HERSHEY_SIMPLEX
        encontrados = 0
        for i in range(faces.shape[2]):
            confidence = faces[0, 0, i, 2]
            if confidence > 0.6:
                encontrados += 1
                box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x,y,x1, y1) = box.astype("int")
                
                center_coordinates_detected = (int((x+x1)/2),int((y+y1)/2))
                
                diff_X = image_center[0] - center_coordinates_detected[0]
                diff_Y = image_center[1] - center_coordinates_detected[1]
                
                cv.circle(img, center_coordinates_detected, 5, (255,255,0), 2)
                
                cv.rectangle(img,(x,y),(x1, y1),(255,0,0),2)
                
                self.determina_target(diff_X, diff_Y)

            # eyes = self.eye_classifier.detectMultiScale(roi_gray)
            # for (ex,ey,ew,eh) in eyes:
            #     cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        if encontrados == 0:
            self.nao_encontrado()
        return img
    @staticmethod
    def createCascadeClassifier_face():
        #return cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_upperbody.xml')
        return cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
        #return cv.CascadeClassifier("lib\haarcascades\haarcascade_frontalface_default.xml")

    @staticmethod
    def createCascadeClassifier_olhos():
        return cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_eye.xml')
        #return cv.CascadeClassifier("lib\haarcascades\haarcascade_eye.xml")