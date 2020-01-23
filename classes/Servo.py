import RPi.GPIO as GPIO
from time import sleep
import logging

class Servo:
	""" 
	This class lets you control a servo motor.
	It takes 1 GPIO pin to control the pwm.
	"""

	current_angle = 0

	def __init__(self, input, lower):
		self.input = input
		GPIO.setup(self.input, GPIO.OUT)
		self.pwm = GPIO.PWM(self.input, 50)
		self.pwm.start(6.39)

	def turn(self, angle):
		duty = (angle / 180) * 4 + 3
		self.pwm.ChangeDutyCycle(duty)

	def stop_turning(self):
		self.pwm.stop()
