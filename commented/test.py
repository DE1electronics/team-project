import task_one, task_two, bluetooth, release

from ws2812 import WS2812
import pyb
from pyb import Pin, Timer, ADC



task1 = task_one.Mode()
task2 = task_two.Mode()
release = release.Mode()
bluetooth = bluetooth.Mode()
modes =[task1, task2, release]
mode = task2
mode_no = 2

while True:
	'''bluetooth.loop()
	if bluetooth.key_press in (0, 1, 2, 3):
		mode = modes[bluetooth.key_press]
		mode_no = bluetooth.key_press
		print('pressed', str(bluetooth.key_press))'''
	mode.loop()
	print(mode_no)