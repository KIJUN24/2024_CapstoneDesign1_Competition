from DOGZILLALib import DOGZILLA

g_dog = DOGZILLA()

def move_motors():
    motor_ids = [11, 12, 13, 21, 22, 23, 31, 32, 33, 41, 42, 43]
    angles = [14, 48, 0, 14, 48, 0, 14, 48, 0, 14, 48, 0]
    speed = 30
    
    g_dog.motor_speed(speed)
    
    g_dog.motor(motor_ids, angles)
move_motors()
