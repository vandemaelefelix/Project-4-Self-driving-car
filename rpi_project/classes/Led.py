import RPi.GPIO as GPIO
from time import sleep
import logging

class Led:
	"""
	LED
	"""
	def __init__(self, led):
		self.led = led
		GPIO.setup(self.led, GPIO.OUT)
	
	def on(self, time=None):
		GPIO.output(self.led, GPIO.HIGH)
		if time != None:
			time.sleep(time)
			GPIO.output(self.led, GPIO.LOW)

	def off(self):
		GPIO.output(self.led, GPIO.LOW)

	def blink(self, interval):
		for i in range(5):
			GPIO.output(self.led, GPIO.HIGH)
			time.sleep(interval)
			GPIO.output(self.led, GPIO.LOW)
			time.sleep(interval)