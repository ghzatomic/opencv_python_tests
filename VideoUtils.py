import numpy as np 
import cv2 as cv

class VideoUtils:

    def __init__(self):
        pass

    def videoCapture(self, videoTransformerFunction=None):
        cap = cv.VideoCapture(0)
        scale_percent = 60 # percent of original size
        while 1:
            ret, img = cap.read()
            # width = int(img.shape[1] * scale_percent / 100)
            # height = int(img.shape[0] * scale_percent / 100)
            # dim = (width, height)
            # resized = cv.resize(img, dim, interpolation = cv.INTER_AREA)
            if videoTransformerFunction:
                img = videoTransformerFunction(img)
            cv.imshow('img',img)
            k = cv.waitKey(30) & 0xff
            if k == 27:
                break

        cap.release()
        cv.destroyAllWindows()

    @staticmethod
    def createCascadeClassifier_face():
        return cv.CascadeClassifier("lib\haarcascades\haarcascade_frontalface_default.xml")

    @staticmethod
    def createCascadeClassifier_olhos():
        return cv.CascadeClassifier("lib\haarcascades\haarcascade_eye.xml")
