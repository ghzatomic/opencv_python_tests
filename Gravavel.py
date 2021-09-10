import cv2

class Gravavel:
    def __init__(self, video_encontrados_path="/Dados/public/videos"):
        self.out = None
        self.fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        self.detection_count = 0
        self.video_encontrados_path = video_encontrados_path
        self.tamanho = (640,480)
        
    def add_encontrado(self):
        self.detection_count += 1
        
    def grava(self, image):
        if self.out == None:
            self.add_encontrado()
            if self.video_encontrados_path:
                self.out = cv2.VideoWriter(self.video_encontrados_path+'/output_'+str(self.detection_count)+'.mp4', self.fourcc, 20.0, self.tamanho)
        if self.out:
            print("Gravando")
            self.out.write(image)
            
    def para_gravacao(self):
        if self.out:
            self.out.release()
            self.out = None
        