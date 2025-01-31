from DOGZILLALib import DOGZILLA

class DogzillaMotorController:
    def __init__(self, speed=30):
        self.dogzilla = DOGZILLA()
        self.speed = speed

    def set_speed(self, speed):
        self.speed = speed
        self.dogzilla.motor_speed(self.speed)

    def move_motors(self, angles):
        motor_ids = [11, 12, 13, 21, 22, 23, 31, 32, 33, 41, 42, 43]
        self.dogzilla.motor_speed(self.speed)
        self.dogzilla.motor(motor_ids, angles)

if __name__ == "__main__":
    motor_controller = DogzillaMotorController(speed=30)
    
    motor_controller.set_speed(30)
    
    angles = [-50, 95, 0, -50, 95, 0, -50, 95, 0, -50, 95, 0]
    
    motor_controller.move_motors(angles)