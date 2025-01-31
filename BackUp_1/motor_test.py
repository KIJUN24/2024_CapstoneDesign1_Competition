#!/usr/bin/env python3
# coding=utf-8

from DOGZILLALib import DOGZILLA

# Initialize the DOGZILLA object
g_dog = DOGZILLA()

def move_motors():
    # Example motor positions and speed
    motor_ids = [11, 12, 13, 21, 22, 23, 31, 32, 33, 41, 42, 43]
    angles = [14, 48, 0, 14, 48, 0, 14, 48, 0, 14, 48, 0]  # Adjust as needed
    speed = 30  # Adjust the speed as needed
    
    # Set motor speed
    g_dog.motor_speed(speed)
    
    # Move motors to the specified angles
    g_dog.motor(motor_ids, angles)
    print("Motors moved to specified angles.")

# Call the function to move motors directly
move_motors()
