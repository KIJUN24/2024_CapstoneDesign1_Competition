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
        cv.imshow("HSV Test", frame2hsv)
        cv.imshow("Line Test", frame_with_lines)

        # Move motors if line is detected
        if line_detected and climbing_step == 0:
            # [Calf, Thigh, Shoulder]
            # [leftF(3), rightF(3), leftR(3), rightR(3)]
            climbing_start = [14, 48, 0, 14, 48, 0, 14, 48, 0, 14, 48, 0]
            motor_controller.move_motors(climbing_start)
            climbing_step = 1
            time.sleep(3)
            climbing = True

            # ready
            if climbing and climbing_step == 1:
                climbing_next_level = [16, 25, 0, 16, 25, 0, 16, 25, 0, 16, 25, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 2

            # start    
            if climbing and climbing_step == 2:
                climbing_next_level = [16, 25, 0, -45, 40, 0, 16, 25, 0, 16, 25, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 3

            if climbing and climbing_step == 3:
                climbing_next_level = [16, 25, 0, -45, -25, 0, 16, 25, 0, 16, 25, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 4

            if climbing and climbing_step == 4:
                climbing_next_level = [16, 25, 0, 55, -25, 0, 16, 25, 0, 16, 25, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 5
            ################### right end ##################


            if climbing and climbing_step == 5:
                climbing_next_level = [-45, 25, 0, 55, -25, 0, 16, 25, 0, 16, 25, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 6

            if climbing and climbing_step == 6:
                climbing_next_level = [-50, -50, 0, 55, -25, 0, 16, 25, 0, 16, 25, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 7

            if climbing and climbing_step == 7:
                climbing_next_level = [55, -25, 0, 55, -25, 0, 16, 25, 0, 16, 25, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 8
            ################### left end ###################

            ################### 1st floor end ###################


            ################### 2nd floor start ###################
            if climbing and climbing_step == 8:
                climbing_next_level = [16, 25, 0, -45, 40, 0, 14, 48, 0, 14, 48, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 9

            if climbing and climbing_step == 9:
                climbing_next_level = [16, 25, 0, -45, -25, 0, 14, 48, 0, 14, 48, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 10

            if climbing and climbing_step == 10:
                climbing_next_level = [16, 25, 0, 55, -25, 0, 14, 48, 0, 14, 48, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 11
            # ################### right end ###################

            if climbing and climbing_step == 11:
                climbing_next_level = [-45, 25, 0, 55, -25, 0, 14, 48, 0, 14, 48, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 12

            if climbing and climbing_step == 12:
                climbing_next_level = [-50, -50, 0, 55, -25, 0, 14, 48, 0, 14, 48, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 13

            if climbing and climbing_step == 13:
                climbing_next_level = [55, -30, 0, 55, -30, 0, 14, 48, 0, 14, 48, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 14

            # ################### rear up ###################
            if climbing and climbing_step == 14:
                climbing_next_level = [55, -30, 0, 55, -30, 0, 16, 48, 0, 16, 48, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 15

            # ################### front down ###################
            if climbing and climbing_step == 15:
                climbing_next_level = [-15, 30, 0, -15, 30, 0, 16, 48, 0, 16, 48, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 16            

            # ################### 3th floor start ###################
            if climbing and climbing_step == 16:
                climbing_next_level = [-15, 30, 0, -65, 30, 0, 16, 48, 0, 16, 48, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 17

            if climbing and climbing_step == 17:
                climbing_next_level = [-15, 30, 0, -65, -25, 0, 16, 48, 0, 16, 48, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 18

            if climbing and climbing_step == 18:
                climbing_next_level = [-15, 30, 0, 35, -25, 0, 16, 48, 0, 16, 48, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 19
            # ################### right end ###################

            # ################### left start ###################
            if climbing and climbing_step == 19:
                climbing_next_level = [-65, 30, 0, 35, -25, 0, 16, 48, 0, 16, 48, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 20

            if climbing and climbing_step == 20:
                climbing_next_level = [-65, -25, 0, 35, -25, 0, 16, 48, 0, 16, 48, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 21

            if climbing and climbing_step == 21:
                climbing_next_level = [35, -25, 0, 35, -25, 0, 16, 48, 0, 16, 48, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(4)
                climbing_step = 22


            # ####### 20241112 ########
            if climbing and climbing_step == 22:
                climbing_next_level = [35, -25, 0, 35, -25, 0, 16, 93, 0, 16, 93, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(4)
                climbing_step = 23

            if climbing and climbing_step == 23:
                climbing_next_level = [35, -25, 0, 35, -25, 0, 16, 93, 0, -73, 93, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(4)
                climbing_step = 24
            
            if climbing and climbing_step == 24:
                climbing_next_level = [35, -25, 0, 35, -25, 0, 16, 93, 0, -37, 93, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(4)
                climbing_step = 25


            # ####### 20241125 ########
            if climbing and climbing_step == 25:
                climbing_next_level = [35, -15, 0, 35, -15, 0, 16, 93, 0, -37, 93, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 26

            if climbing and climbing_step == 26:
                climbing_next_level = [35, -15, 0, 35, -15, 0, -37, 93, 0, -37, 93, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 27

            if climbing and climbing_step == 27:
                climbing_next_level = [35, -15, 0, 35, -15, 0, 14, 48, 0, 14, 48, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 28

            if climbing and climbing_step == 28:
                climbing_next_level = [35, -15, 0, 35, -15, 0, 14, 48, 0, 14, 48, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 29
            
            if climbing and climbing_step == 29:
                climbing_next_level = [50, -66, 0, 50, -66, 0, 14, 48, 0, 14, 48, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 30


            # ####### 20241127 ########
            if climbing and climbing_step == 30:
                climbing_next_level = [50, -66, 0, 50, -66, 0, 35, 48, 0, 14, 48, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 31
            
            if climbing and climbing_step == 31:
                climbing_next_level = [50, -66, 0, 50, -66, 0, 35, 48, 0, 14, 60, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 32

            if climbing and climbing_step == 32:
                climbing_next_level = [50, -66, 0, 50, -66, 0, 35, 48, 0, -45, 60, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 33
            
            if climbing and climbing_step == 33:
                climbing_next_level = [50, -66, 0, 50, -66, 0, 35, 48, 0, -20, 60, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 34

            if climbing and climbing_step == 34:
                climbing_next_level = [50, -60, 0, 50, -60, 0, 35, 48, 0, -20, 60, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 35

            if climbing and climbing_step == 35:
                climbing_next_level = [50, -60, 0, 50, -60, 0, 35, 48, 0, 0, 60, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 36

            if climbing and climbing_step == 36:
                climbing_next_level = [50, -60, 0, 50, -60, 0, -43, 93, 0, 0, 60, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 37

            ######## 20241128 ########
            if climbing and climbing_step == 37:
                climbing_next_level = [50, -60, 0, 50, -60, 0, -43, 93, 0, 0, 60, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 38

            if climbing and climbing_step == 38:
                climbing_next_level = [50, -60, 0, 50, -60, 0, 0, 60, 0, 0, 60, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 39

            if climbing and climbing_step == 39:
                climbing_next_level = [14, 48, 0, 14, 48, 0, 14, 48, 0, 14, 48, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 40 

            if climbing and climbing_step == 40:
                climbing_next_level = [14, 48, 0, 14, 48, 0, 14, 48, 0, 14, 48, 0]
                motor_controller.move_motors(climbing_next_level)
                time.sleep(3)
                climbing_step = 41


        
            
            # ################### rear leg start_1 ###################
            # if climbing and climbing_step == 22:
            #     climbing_next_level = [35, -25, 0, 35, -25, 0, -20, 48, 0, 16, 48, 0]
            #     motor_controller.move_motors(climbing_next_level)
            #     time.sleep(4)
            #     climbing_step = 23
            
            # if climbing and climbing_step == 23:
            #     climbing_next_level = [35, -25, 0, 35, -25, 0, -20, 48, 0, -20, 48, 0]
            #     motor_controller.move_motors(climbing_next_level)
            #     time.sleep(4)
            #     climbing_step = 24

            # if climbing and climbing_step == 24:
            #     climbing_next_level = [35, -25, 0, 35, -25, 0, 16, 48, 0, 16, 48, 0]
            #     motor_controller.move_motors(climbing_next_level)
            #     time.sleep(4)
            #     climbing_step = 25

            # ################### rear leg start_2 ###################
            # if climbing and climbing_step == 25:
            #     climbing_next_level = [35, -25, 0, 35, -25, 0, -25, 48, 0, 16, 48, 0]
            #     motor_controller.move_motors(climbing_next_level)
            #     time.sleep(4)
            #     climbing_step = 26
            
            # if climbing and climbing_step == 26:
            #     climbing_next_level = [35, -25, 0, 35, -25, 0, -25, 48, 0, -25, 48, 0]
            #     motor_controller.move_motors(climbing_next_level)
            #     time.sleep(4)
            #     climbing_step = 27

            # if climbing and climbing_step == 27:
            #     climbing_next_level = [35, -25, 0, 35, -25, 0, 16, 48, 0, 16, 48, 0]
            #     motor_controller.move_motors(climbing_next_level)
            #     time.sleep(4)
            #     climbing_step = 28

            # ################### rear leg start_3 ###################
            # if climbing and climbing_step == 28:
            #     climbing_next_level = [35, -25, 0, 35, -25, 0, -25, 48, 0, 16, 48, 0]
            #     motor_controller.move_motors(climbing_next_level)
            #     time.sleep(4)
            #     climbing_step = 29
            
            # if climbing and climbing_step == 29:
            #     climbing_next_level = [35, -25, 0, 35, -25, 0, -25, 48, 0, -25, 48, 0]
            #     motor_controller.move_motors(climbing_next_level)
            #     time.sleep(4)
            #     climbing_step = 30


            # ################### climbing end ###################
            # if climbing and climbing_step == 30:
            #     climbing_next_level = [14, 48, 0, 14, 48, 0, 14, 48, 0, 14, 48, 0]
            #     motor_controller.move_motors(climbing_next_level)
            #     time.sleep(3)
            #     climbing_step = 31


            # ################### wave a hand ###################
            # if climbing and climbing_step == 31:
            #     climbing_next_level = [14, 48, 0, 14, 48, 0, -10, 48, 0, -10, 48, 0]
            #     motor_controller.move_motors(climbing_next_level)
            #     time.sleep(1.5)
            #     climbing_step = 32

            # if climbing and climbing_step == 31:
            #     climbing_next_level = [-25, 20, 0, 14, 48, 0, -10, 48, 0, -10, 48, 0]
            #     motor_controller.move_motors(climbing_next_level)
            #     time.sleep(1.5)
            #     climbing_step = 32

            # if climbing and climbing_step == 32:
            #     climbing_next_level = [-25, 20, 15, 14, 48, 0, -10, 48, 0, -10, 48, 0]
            #     motor_controller.move_motors(climbing_next_level)
            #     time.sleep(1.5)
            #     climbing_step = 33

            # if climbing and climbing_step == 33:
            #     climbing_next_level = [-25, 20, -15, 14, 48, 0, -10, 48, 0, -10, 48, 0]
            #     motor_controller.move_motors(climbing_next_level)
            #     time.sleep(1.5)
            #     climbing_step = 34

            # if climbing and climbing_step == 34:
            #     climbing_next_level = [-25, 20, 15, 14, 48, 0, -10, 48, 0, -10, 48, 0]
            #     motor_controller.move_motors(climbing_next_level)
            #     time.sleep(1.5)
            #     climbing_step = 35

            # if climbing and climbing_step == 35:
            #     climbing_next_level = [-25, 20, -15, 14, 48, 0, -10, 48, 0, -10, 48, 0]
            #     motor_controller.move_motors(climbing_next_level)
            #     time.sleep(1.5)
            #     climbing_step = 36

            # if climbing and climbing_step == 36:
            #     climbing_next_level = [-25, 20, 15, 14, 48, 0, -10, 48, 0, -10, 48, 0]
            #     motor_controller.move_motors(climbing_next_level)
            #     time.sleep(1.5)
            #     climbing_step = 37

            # if climbing and climbing_step == 37:
            #     climbing_next_level = [-25, 20, -15, 14, 48, 0, -10, 48, 0, -10, 48, 0]
            #     motor_controller.move_motors(climbing_next_level)
            #     time.sleep(1.5)
            #     climbing_step = 38
            
            # if climbing and climbing_step == 38:
            #     climbing_next_level = [14, 48, 0, 14, 48, 0, 14, 48, 0, 14, 48, 0]
            #     motor_controller.move_motors(climbing_next_level)
            #     time.sleep(3)
            #     climbing_step = 39

            # ################### rear leg start_3 ###################
            # if climbing and climbing_step == 39:
            #     climbing_next_level = [57, -50, 0, 57, -50, 0, 14, 48, 0, 14, 48, 0]
            #     motor_controller.move_motors(climbing_next_level)
            #     time.sleep(3)
            #     climbing_step = 40

            # while climbing:
            #     print("climbing start")
            #     if not line_detected:
            #         climbing = False

        # Exit condition
        k = cv.waitKey(1) & 0xFF
        if k == 27 or k == ord('q'):
            break

    del camera
    cv.destroyAllWindows()