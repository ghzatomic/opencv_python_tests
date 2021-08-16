from SistemaMira import ObjectDetector as MiraYolov4
from FaceDetectorMiraDNN import FaceDetectorMira
from YoloV4ObjectDetector import ObjectDetector
from VideoUtils import VideoUtils

face_detector = FaceDetectorMira(True)
detector_pessoa = MiraYolov4()
object_detector = ObjectDetector()
video_utils = VideoUtils()

image_path = "imagem/captcha3.jpeg"

def detector_pessoa_func(img):
    return detector_pessoa.detectaImagemCV2(img)

def face_detector_func(img):
    return face_detector.detectaFace2(img)

def obj_detector_func(img):
    return object_detector.detectaImagemCV2(img)

def main():
    video_utils.videoCapture(face_detector_func)

def image_test():
    object_detector.detectaImagem(image_path, show=True)


if "__main__":
    main()
    #image_test()