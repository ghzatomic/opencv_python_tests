import numpy as np 
import cv2 as cv
import time
from BluetoothArduinoCommunication import BluetoothArduinoCommunication

class FaceDetectorMira(BluetoothArduinoCommunication):

    def __init__(self):
        BluetoothArduinoCommunication.__init__(self)
        self.face_classifier = FaceDetectorMira.createCascadeClassifier_face()
        self.eye_classifier = FaceDetectorMira.createCascadeClassifier_olhos()
        #self.connect_bt = False

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
        image_center = (int(W/2) , int(H/2))
        color_image_center = (0, 255, 0)
        start = time.time()
        faces = self.face_classifier.detectMultiScale(gray, 1.3, 5)
        end = time.time()
        #print("[INFO] {:.6f} seconds".format(end - start))
        cv.circle(img, image_center, 5, color_image_center, 2)
        for (x,y,w,h) in faces:
            center_coordinates_detected = (int(x+w/2),int(y+h/2))
            
            diff_X = image_center[0] - center_coordinates_detected[0]
            diff_Y = image_center[1] - center_coordinates_detected[1]
            
            cv.circle(img, center_coordinates_detected, 5, (255,0,0), 2)
            
            cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            
            self.determina_target(diff_X, diff_Y)

            #eyes = self.eye_classifier.detectMultiScale(roi_gray)
            #for (ex,ey,ew,eh) in eyes:
            #    cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    
        return img
    @staticmethod
    def createCascadeClassifier_face():
        return cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
        #return cv.CascadeClassifier("lib\haarcascades\haarcascade_frontalface_default.xml")

    @staticmethod
    def createCascadeClassifier_olhos():
        return cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_eye.xml')
        #return cv.CascadeClassifier("lib\haarcascades\haarcascade_eye.xml")
