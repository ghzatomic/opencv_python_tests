import numpy as np 
import cv2 as cv

class VideoUtils:

    def __init__(self):
        pass
    
    def returnCameraIndexes(self):
        index = 0
        arr = []
        i = 10
        while i > 0:
            cap = cv.VideoCapture(index)
            if cap.read()[0]:
                arr.append(index)
                cap.release()
            index += 1
            i -= 1
        return arr

    def videoCapture(self, videoTransformerFunction=None):
        print(self.returnCameraIndexes())
        cap = cv.VideoCapture(3)
        scale_percent = 60 # percent of original size
        while 1:
            ret, img = cap.read()
            img = cv.flip(img, 1)
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
