from SistemaMira import ObjectDetector as MiraYolov4
from FaceDetectorMiraDNN import FaceDetectorMira
from YoloV4ObjectDetector import ObjectDetector
#from YoloV5ObjectDetector import ObjectDetector as ObjectDetectorV5
from VideoUtils import VideoUtils
from HumanoMira import HumanoMira

connect = True
camera_index = 3 #Linux Camera
#camera_index = 1 ## Windows com a camera
print_cameras_disponiveis = True

video_encontrados_path = None#"/Dados/public/videos/"

yolo_path = "yolo/yolov4tiny"
#yolo_path = "yolo/yolov4optimal"

serial_port = '/dev/ttyUSB0' # Linux
#serial_port = 'COM4' # Windows

ativa_laser = True

allowed_classes = ['person',"cat",
"dog",
"car;",
"bird",
"horse",
"bicycle",
"motorbike"]

face_detector = FaceDetectorMira(connect, serial_port=serial_port, video_encontrados_path=video_encontrados_path, ativa_laser=ativa_laser)
detector_pessoa = MiraYolov4(connect, allowed_classes= ['person'], serial_port=serial_port, yolo_path=yolo_path, video_encontrados_path=video_encontrados_path, ativa_laser=ativa_laser)
object_detector = ObjectDetector()
video_utils = VideoUtils()

image_path = "imagem/image.jpeg"

def detector_pessoa_func(img): #MELHOR
    return detector_pessoa.detectaImagemCV2(img)

def face_detector_func(img):
    return face_detector.detectaFace2(img)

def obj_detector_func(img):
    return object_detector.detectaImagemCV2(img)

def main():
    video_utils.videoCapture(camera_index, videoTransformerFunction=face_detector_func, print_cameras_disponiveis=print_cameras_disponiveis)

def image_test():
    face_detector.detectaImagem(image_path)


if "__main__":
    main()
    #image_test()