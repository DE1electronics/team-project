import pyb
from pyb import UART

class Mode:
    def __init__(self):
        self.s1 = pyb.Servo(3)   #defining the servo motor
        self.initial_angle = -70
        self.final_angle = 10
        self.s1.angle(self.initial_angle)   #setting the servo motor to start position

    def loop(self):           #function to release elastic band using servo motor and then reset it
        self.s1.angle(self.final_angle)
        pyb.delay(1000)
        self.s1.angle(self.initial_angle)

    def __repr__(self):
        return 'release'