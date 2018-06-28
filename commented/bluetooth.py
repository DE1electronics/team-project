from pyb import UART

class Mode():
	def __init__(self):
		#bluetooth communication
		self.key = (0, 1, 2, 3, 'U', 'D', 'L', 'R')
		self.uart = UART(6)
		self.uart.init(9600, bits = 8, parity = None, stop = 2)
		self.key_press = None

	def loop(self):
		if self.uart.any() > 5:   #wait for a message to be sent
		    self.command = self.uart.read(5)   #read the message which was sent
		    self.key_index = self.command[2] - ord('1')      #convert ascii character send to an index for the list of keys
		    if 0 <= self.key_index <= 7:  # checks the index is valid
		        self.key_press = self.key[self.key_index]

		    print("You've selected: ", str(self.key_press))    #print what is being pressed
