import cv2 as cv
import numpy as np

class DogzillaCamera:
    def __init__(self, video_id=1, width=640, height=480, debug=False):
        self.__debug = debug
        self.__video_id = video_id
        self.__state = False
        self.__width = width
        self.__height = height
        self.yellow_lower = np.array([0, 0, 0])
        self.yellow_upper = np.array([255, 255, 255])
        self.__video = cv.VideoCapture(self.__video_id)
        success = self.__video.isOpened()
        if not success:
            self.__video_id = (self.__video_id + 1) % 2
            self.__video = cv.VideoCapture(self.__video_id)
            success = self.__video.isOpened()
            if not success and self.__debug:
                return
        self.__state = True
        self.__config_camera()

    def __del__(self):
        self.__video.release()
        self.__state = False

    def __config_camera(self):
        cv_edition = cv.__version__
        if cv_edition[0] == '3':
            self.__video.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'XVID'))
        else:
            self.__video.set(cv.CAP_PROP_FOURCC, cv.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        self.__video.set(cv.CAP_PROP_FRAME_WIDTH, self.__width)
        self.__video.set(cv.CAP_PROP_FRAME_HEIGHT, self.__height)

    def isOpened(self):
        return self.__video.isOpened()

    def get_frame(self):
        success, image = self.__video.read()
        return success, image

if __name__ == '__main__':
    camera = DogzillaCamera(debug=True)

    while camera.isOpened():
        ret, frame = camera.get_frame()
        if not ret:
            break
        
        k = cv.waitKey(1) & 0xFF
        if k == 27 or k == ord('q'):
            break

    del camera
    cv.destroyAllWindows()