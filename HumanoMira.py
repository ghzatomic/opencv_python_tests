import numpy as np 
import cv2 as cv
import imutils
from imutils.object_detection import non_max_suppression
import time
from time import sleep
from BluetoothArduinoCommunication import BluetoothArduinoCommunication

class HumanoMira(BluetoothArduinoCommunication):

    def __init__(self, connect_bt=False):
        BluetoothArduinoCommunication.__init__(self)
        self.connect = False
        self.hog = cv.HOGDescriptor()
        self.hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

    def detectaImagem(self, imagePath, show=True):
        image = cv.imread(imagePath)
        image = self.detecta(image)
        if show:
            cv.imshow("Image", image)
            cv.waitKey(0)

            cv.destroyAllWindows()
            
        return image

    def detecta(self,img):
        if not self.connected:
            self.do_connect()
        # resizing for faster detection
        img = imutils.resize(img, width=min(800,img.shape[1]))
        gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        #gray = cv.GaussianBlur(gray, (5, 5), 0)
        
        (H, W) = img.shape[:2]
        image_center = (int(W/2) , int(H/2))
        color_image_center = (0, 255, 0)
        start = time.time()
        boxes, weights = self.hog.detectMultiScale(img, winStride = (8, 8))
        end = time.time()
        #print("[INFO] {:.6f} seconds".format(end - start))
        cv.circle(img, image_center, 5, color_image_center, 2)
        if len(boxes) == 0:
            self.nao_encontrado()
        else:
            boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
            pick = non_max_suppression(boxes, probs=None, overlapThresh=0.65)
            for (x,y,w,h) in pick:
                
                cv.rectangle(img, (x,y), (w,h), (0,255,0), 2)
                
                center_coordinates_detected = (int((x+w)/2),int((y+h)/2))
                
                diff_X = image_center[0] - center_coordinates_detected[0]
                diff_Y = image_center[1] - center_coordinates_detected[1]
                
                cv.circle(img, center_coordinates_detected, 5, color_image_center, 2)
        return img
