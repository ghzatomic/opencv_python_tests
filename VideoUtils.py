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
            cap = cv.VideoCapture(index, cv.CAP_ANY)
            if cap.read()[0]:
                width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
                
                arr.append({"indice":index, "w":str(width), "h":str(height)})
                cap.release()
            index += 1
            i -= 1
        return arr

    def videoCapture(self, index, videoTransformerFunction=None, print_cameras_disponiveis=True, use_dshow=False):
        if print_cameras_disponiveis:
            print(self.returnCameraIndexes())
        cap = cv.VideoCapture(index, cv.CAP_DSHOW if use_dshow else cv.CAP_ANY)# Linux com camera
        #cap = cv.VideoCapture(1, cv.CAP_ANY)
        #cap = cv.VideoCapture(0, cv.CAP_DSHOW)# Windows com a camera
        #ret_val = cap.set(cv.CAP_PROP_ZOOM, 0x8004)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)
        scale_percent = 60 # percent of original size
        while 1:
            if not cap.isOpened():
                continue
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

