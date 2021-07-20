from SistemaMira import ObjectDetector
from FaceDetectorMira import FaceDetectorMira
from VideoUtils import VideoUtils

face_detector = FaceDetectorMira()
object_detector = ObjectDetector()
video_utils =VideoUtils()

image_path = "imagem/TESTEcafe.jpeg"


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