import pyb
from pyb import Pin, Timer, ADC
import move

class Mode():
	def __init__(self, robot):
		self.pathBlocked = False
		self.robot = robot

	def checkBlocked(self):
		if not(self.robot.IR1.value() and self.robot.IR2.value()):
			return True
		else:
			return False

	def loop(self):
		if self.pathBlocked:
			self.robot.stop()
			self.robot.rotateLeft()
		else:
			self.robot.moveForwards()
			self.robot.updateSpeed()
		pyb.delay(50)
		self.pathBlocked = self.checkBlocked()