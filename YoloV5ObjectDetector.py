import numpy as np 
import cv2
import time
import os
import torch

yolo_path = "yolo/yolov5"

labelsPath = os.path.sep.join([yolo_path, "coco.names"])
weightsPath = os.path.sep.join([yolo_path, "yolov5l6.pt"])

class ObjectDetector:

    def __init__(self):
        self.confidence_thresold = 0.5
        self.thresold = 0.3
        self.LABELS = open(labelsPath).read().strip().split("\n")
        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3),
            dtype="uint8")
        self.net = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True, classes=len(self.LABELS))  # or yolov5m, yolov5l, yolov5x, custom
        
        #model = torch.hub.load('ultralytics/yolov5', 'custom', path=weightsPath, source='local') 
        
        #self.net.load_state_dict(torch.load('...')['model'].state_dict())
        #model.load_state_dict(torch.load('yolov5s_10cls.pt')['model'].state_dict())

        #self.net = model.fuse().autoshape()
        
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
        
        results = self.net(image)

        # Results
        results = self.isola_scores(results)
        self.plot_boxes(results, image)
        return image
    
    def isola_scores(self, results):
        labels, cord = results.xyxyn[0][:, -1].numpy(), results.xyxyn[0][:, :-1].numpy()
        return labels, cord

    def class_to_label(self, x):
        return self.LABELS[int(x)]

    def plot_boxes(self, results, frame):
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.2:
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, self.class_to_label(labels[i]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)

    