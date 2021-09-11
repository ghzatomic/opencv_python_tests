import cv2
from datetime import datetime

class Gravavel:
    def __init__(self, video_encontrados_path="/Dados/public/videos"):
        self.out = None
        self.fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        #self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        #self.fourcc = cv2.VideoWriter_fourcc(*'MPEG')
        self.detection_count = 0
        self.video_encontrados_path = video_encontrados_path
        
    def add_encontrado(self):
        self.detection_count += 1
        
    def grava(self, image):
        if self.out == None:
            self.add_encontrado()
            if self.video_encontrados_path:
                now = datetime.now()
                date_time = now.strftime("%m%d%Y%H%M%S")
                size = image.shape[1], image.shape[0]
                self.out = cv2.VideoWriter(self.video_encontrados_path+'/output'+date_time+'_'+str(self.detection_count)+'.mp4', self.fourcc, 60, size)
        if self.out:
            print("Gravando")
            self.out.write(image)
            
    def para_gravacao(self):
        if self.out:
            self.out.release()
            self.out = None
        