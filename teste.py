from SistemaMira import ObjectDetector as MiraYolov4
from FaceDetectorMiraDNN import FaceDetectorMira
from YoloV4ObjectDetector import ObjectDetector
#from YoloV5ObjectDetector import ObjectDetector as ObjectDetectorV5
from VideoUtils import VideoUtils
from HumanoMira import HumanoMira

connect = True

face_detector = FaceDetectorMira(connect)
detector_pessoa = MiraYolov4(connect)
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
    video_utils.videoCapture(detector_pessoa_func)

def image_test():
    face_detector.detectaImagem(image_path)


if "__main__":
    main()
    #image_test()