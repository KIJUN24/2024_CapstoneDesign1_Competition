#!/usr/bin/env python3
# coding=utf-8

from DOGZILLALib import DOGZILLA

class DogzillaMotorController:
    def __init__(self, speed=30):
        # Initialize the DOGZILLA robot
        self.dogzilla = DOGZILLA()
        self.speed = speed

    def set_speed(self, speed):
        """Set the motor speed."""
        self.speed = speed
        self.dogzilla.motor_speed(self.speed)
        print(f"Motor speed set to {self.speed}")

    def move_motors(self, angles):
        """
        Move the motors to the specified angles.

        Parameters:
        - angles: A list of angles for each motor in the order [11, 12, 13, 21, 22, 23, 31, 32, 33, 41, 42, 43].
        """
        motor_ids = [11, 12, 13, 21, 22, 23, 31, 32, 33, 41, 42, 43]
        
        # Ensure the angles list has the right number of values
        if len(angles) != len(motor_ids):
            raise ValueError("Angles list must contain 12 values.")
        
        # Set motor speed
        self.dogzilla.motor_speed(self.speed)
        
        # Move motors to the specified angles
        self.dogzilla.motor(motor_ids, angles)
        print(f"Motors moved to specified angles: {angles}")

# Usage Example
if __name__ == "__main__":
    # Initialize the motor controller with a speed of 30
    motor_controller = DogzillaMotorController(speed=30)
    
    # Set motor speed (optional, as it's already set in the initializer)
    motor_controller.set_speed(30)
    
    # Define angles for each motor
    # [Calf, Thigh, Shoulder]
    angles = [-50, 95, 0, -50, 95, 0, -50, 95, 0, -50, 95, 0]  # Adjust as needed
    
    # Move motors directly to these angles
    motor_controller.move_motors(angles)
