#!/usr/bin/env python3
# coding=utf-8

import cv2 as cv
import numpy as np
from DOGZILLALib import DOGZILLA
import time

class DogzillaMotorController:
    def __init__(self, speed=30):
        self.dogzilla = DOGZILLA()
        try:    
            motor_controller = DogzillaMotorController(speed=30)
            self.speed = speed
            motor_controller.set_speed(self.speed)
            angles = [-50, 95, 0, -50, 95, 0, -40, 95, 0, -40, 95, 0]
            motor_controller.move_motors(angles)
        except Exception as e:
            print(f"Error initializig motors: {e}")


    def set_speed(self, speed):
        self.speed = speed
        self.dogzilla.motor_speed(self.speed)
        print(f"Motor speed set to {self.speed}")

    def move_motors(self, angles):
        motor_ids = [11, 12, 13, 21, 22, 23, 31, 32, 33, 41, 42, 43]
        if len(angles) != len(motor_ids):
            raise ValueError("Angles list must contain 12 values.")
        self.dogzilla.motor_speed(self.speed)
        self.dogzilla.motor(motor_ids, angles)
        print(f"Motors moved to specified angles: {angles}")

# Camera Class with Line Detection
class DogzillaCamera:
    def __init__(self, video_id=1, width=640, height=480, debug=False):
        self.__debug = debug
        self.__video_id = video_id
        self.__state = False
        self.__width = width
        self.__height = height
        self.yellow_lower = np.array([15, 80, 0])
        self.yellow_upper = np.array([45, 255, 255])
        self.__video = cv.VideoCapture(self.__video_id)
        success = self.__video.isOpened()
        if not success:
            self.__video_id = (self.__video_id + 1) % 2
            self.__video = cv.VideoCapture(self.__video_id)
            success = self.__video.isOpened()
            if not success and self.__debug:
                print("---------Camera Init Error!------------")
                return
        self.__state = True
        self.__config_camera()
        if self.__debug:
            print(f"---------Video{self.__video_id} Init OK!------------")

    def __del__(self):
        if self.__debug:
            print("---------Del Camera!------------")
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

    def detect_color(self, frame):
        img_line_roi = frame.copy()[150:350, :]
        hsv_line = cv.cvtColor(img_line_roi, cv.COLOR_BGR2HSV)
        yellow_mask = cv.inRange(hsv_line, self.yellow_lower, self.yellow_upper)
        blend_color = cv.bitwise_and(hsv_line, hsv_line, mask=yellow_mask)
        self.img_roi = cv.cvtColor(blend_color, cv.COLOR_HSV2BGR)
        cv.imshow("RGB", frame)
        cv.imshow("ROI", img_line_roi)


        return self.img_roi

    def detect_line(self, frame):
        gray = cv.cvtColor(self.img_roi, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray, (27, 27), 0)
        edge = cv.Canny(np.uint8(blur), 10, 30)
        lines = cv.HoughLinesP(edge, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)
        line_detected = False

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                line_detected = True

        return frame, line_detected



if __name__ == '__main__':
    camera = DogzillaCamera(debug=True)
    motor_controller = DogzillaMotorController(speed=30)
    climbing = False
    climbing_step = 0

    while camera.isOpened():
        ret, frame = camera.get_frame()
        if not ret:
            break

        # Detect the line
        frame2hsv = camera.detect_color(frame)
        frame_with_lines, line_detected = camera.detect_line(frame)

        # Display the images

        
        cv.imshow("Line", frame_with_lines)
        cv.imshow("HSV", frame2hsv)

        
        

        # Exit condition
        k = cv.waitKey(1) & 0xFF
        if k == 27 or k == ord('q'):
            break

    del camera
    cv.destroyAllWindows()