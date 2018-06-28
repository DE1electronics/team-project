# -*- coding: utf-8 -*-

from ws2812 import WS2812
import pyb
from pyb import Pin, Timer, ADC

class Colour:
    def __init__(self, r, g, b, brightness = 100):
        self.r = r
        self.g = g
        self.b = b
        self.R = r
        self.G = g
        self.B = b
        self._brightness = brightness
        self.adjust_for_brightness()

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        if value > 255:
            raise ValueError('A brightness greater than 255 is not possible.')
        self._brightness = value
        self.adjust_for_brightness()

    def adjust_for_brightness(self):
        total = self.r + self.g + self.b
        if total:
            self.R = self.r/total * self.brightness
            self.G = self.g/total * self.brightness
            self.B = self.b/total * self.brightness

    def __repr__(self):
        return ("R: {}, G: {}, B: {}".format(self.R, self.G, self.B))

class Mode:
    def __init__(self):
        self.ultrasonic_sensor = ADC(Pin("X4"))
        self.hall_sensor = Pin("X6", Pin.IN)
        self.pot = ADC(Pin("X8"))
        self.ring = WS2812(spi_bus=2, led_count=15)

        self.red = Colour(1, 0, 0)
        self.green = Colour(0.4, 1, 0)
        self.purple = Colour(0.4, 0, 1)
        self.off = Colour(0, 0, 0)

        self.magnet_detected = self.green
        self.ultrasound_detected = self.purple
        self.colour = self.red
        self.HISTORY_DEPTH = 15
        self.history = [0 for i in range(self.HISTORY_DEPTH)] #stores the last few values recorded
        self.i = 0

    def loop(self):
        self.i += 1 #increase the pointer by one
        self.i = self.i % self.HISTORY_DEPTH #ensure that the pointer loops back to 0 when it reaches the end of the list
        if self.ultrasonic_sensor.read() > 2800: #2700 is the threshold voltage, we found the value generally only exceeds 2600 if the ultrasonic sensor is nearby
            self.history[self.i] = 1 #adds a 1 / True value to the history as the sensor has detected ultrasound
        else:
            self.history[self.i] = 0 #adds a 0 / False value as the sensor hasn't detected ultrasound

        #calculates the number of times the ultrasound has been triggered within the alloted time
        self.total = 0
        for x in self.history:
            self.total += x

        #if it's greater than one assume that an ultrasound has been detected
        #however the brightness of the LEDs can reflect the certainty (the more time's it has been triggered within the time, the more certain we are)
        if self.total > 0:
            self.colour = self.ultrasound_detected
            self.colour.brightness = self.total/self.HISTORY_DEPTH*125 #the certainty is reflected in the brightness of the LEDs
        #checks to see if the hall sensor value
        elif not self.hall_sensor.value():
            self.colour = self.magnet_detected
            self.colour.brightness = 100
        else:
            self.colour = self.off
        self.data = [(self.colour.R, self.colour.G, self.colour.B) for i in range(15)]
        self.ring.show(self.data)

    def __repr__(self):
        return 'task_two'
