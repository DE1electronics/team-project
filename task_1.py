import pyb
from pyb import Pin, Timer, ADC

class Motor:
	def __init__(self, out1, out2, pwm, chan):
		self.o1 = Pin(out1, Pin.OUT_PP)
		self.o2 = Pin(out2, Pin.OUT_PP)
		self.pwm = Pin(pwm)
		self.ch = tim.channel(chan, Timer.PWM, pin = self.pwm)
		self.speed = 50

	def forward(self):
		self.o1.high()
		self.o2.low()
		self.ch.pulse_width_percent(self.speed)

	def stop(self):
		self.o1.low()
		self.o2.low()
		self.ch.pulse_width_percent(0)

	def backward(self):
		self.o1.low()
		self.o2.high()
		self.ch.pulse_width_percent(self.speed)

#Defines the pins which the infrared sensors are connected to
IR1 = Pin('X9', Pin.IN)
IR2 = Pin('X10', Pin.IN)

#sets up the timer
tim = Timer(2, freq = 1000)

#Defines the pins that motor A is connected to
A1     = 'Y9'
A2     = 'Y10'
PWMA   = 'X1'
chanA  = 1
motorA = Motor(A1, A2, PWMA, chanA)

#Defines the pins which motor B is connected to
B1     = 'Y11'
B2     = 'Y12'
PWMB   = 'X2'
chanB  = 2
motorB = Motor(B1, B2, PWMB, chanB)

#Initial speed of the robot
speed = 50

#Initial state of the path
pathBlocked = False

#Defines the speed at which the robot rotate
ROTATION_SPEED = 20

#The pin which is connected to the potentiometer
pot = ADC(Pin('X8'))

def moveForwards():
	motorA.forward()
	motorB.forward()

def moveBackwards():
	motorA.backward()
	motorB.backward()

def stop():
	motorA.stop()
	motorB.stop()

def changeSpeed(s):
	motorA.speed = s
	motorB.speed = s

def updateSpeed():
	s = (pot.read() / 4095) * 100
	changeSpeed(s)

def rotateLeft():
	changeSpeed(ROTATION_SPEED)
	motorA.backward()
	motorB.forward()

def rotateRight():
	changeSpeed(ROTATION_SPEED)
	motorA.forward()
	motorB.backward()

def checkBlocked():
	if not(IR1.value() and IR2.value()):
		return True
	else:
		return False

while True:
	if pathBlocked:
		stop()
		rotateLeft()
	else:
		moveForwards()
		updateSpeed()
	pyb.delay(50)
	pathBlocked = checkBlocked()

