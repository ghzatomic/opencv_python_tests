import numpy as np 
import cv2 as cv

class FaceDetector:

    def __init__(self):
        self.face_classifier = FaceDetector.createCascadeClassifier_face()
        self.eye_classifier = FaceDetector.createCascadeClassifier_olhos()

    def FaceDetector(self):
        pass

    def detectaFaceImagem(self, image):
        image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        faces = self.face_classifier.detectMultiScale(image_gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv.rectangle(image, (x,y), (x+w, y+h), (255,0,0), 2)
        return image

    def detectaFace2(self,img):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (5, 5), 0)
        faces = self.face_classifier.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

            eyes = self.eye_classifier.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    
        return img
    @staticmethod
    def createCascadeClassifier_face():
        return cv.CascadeClassifier("lib\haarcascades\haarcascade_frontalface_default.xml")

    @staticmethod
    def createCascadeClassifier_olhos():
        return cv.CascadeClassifier("lib\haarcascades\haarcascade_eye.xml")
