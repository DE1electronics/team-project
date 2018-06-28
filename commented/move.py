import pyb
from pyb import Pin, Timer, ADC

class Motor:
	def __init__(self, out1, out2, pwm, chan, tim):
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
		self.