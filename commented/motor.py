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

class Mode():
	def __init__(self):
		#Defines the pins which the infrared sensors are connected to
		self.IR1 = Pin('X9', Pin.IN)
		self.IR2 = Pin('X10', Pin.IN)

		#sets up the timer
		self.tim = Timer(2, freq = 1000)

		#Defines the pins that motor A is connected to
		self.A1     = 'Y9'
		self.A2     = 'Y10'
		self.PWMA   = 'X1'
		self.chanA  = 1
		self.motorA = Motor(self.A1, self.A2, self.PWMA, self.chanA)

		#Defines the pins which motor B is connected to
		self.B1     = 'Y11'
		self.B2     = 'Y12'
		self.PWMB   = 'X2'
		self.chanB  = 2
		self.motorB = Motor(self.B1, self.B2, self.PWMB, self.chanB)

		#Initial speed of the robot
		self.speed = 50

		#Initial state of the path
		self.pathBlocked = False

		#Defines the speed at which the robot rotate
		self.ROTATION_SPEED = 50

		#The pin which is connected to the potentiometer
		self.pot = ADC(Pin('X8'))

	def moveForwards(self):
		self.motorA.forward()
		self.motorB.forward()

	def moveBackwards(self):
		self.motorA.backward()
		self.motorB.backward()

	def stop(self):
		self.motorA.stop()
		self.motorB.stop()

	def changeSpeed(self,s):
		self.motorA.speed = s
		self.motorB.speed = s

	def updateSpeed(self):
		self.s = (pot.read() / 4095) * 100
		selfchangeSpeed(s)

	def rotateLeft(self):
		self.changeSpeed(self.ROTATION_SPEED)
		self.motorA.backward()
		self.motorB.forward()

	def rotateRight(self):
		self.changeSpeed(self.ROTATION_SPEED)
		self.motorA.forward()
		self.motorB.backward()

	def checkBlocked(self):
		if not(self.IR1.value() and self.IR2.value()):
			return True
		else:
			return False

	def loop(self):
		if self.pathBlocked:
			self.stop()
			self.rotateLeft()
		else:
			self.moveForwards()
			self.updateSpeed()
		pyb.delay(50)
		self.pathBlocked = self.checkBlocked()

