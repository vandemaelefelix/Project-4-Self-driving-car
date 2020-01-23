from classes.Servo import Servo
from classes.DC import DC
from classes.Led import Led

import RPi.GPIO as GPIO
from time import sleep
import logging

class Car:
	"""
	This class lets you control an RC car with 2 DC motors. 
	One for driving and the other one for steering.
	""" 	

	def __init__(self, input1, input2, enable, inputServo, inputLed):
		self.input1 = input1
		self.input2 = input2
		self.enable = enable
		self.inputServo = inputServo
		self.inputLed = inputLed

		self.current_angle = 0

		self.motor1 = DC(self.input1, self.input2, self.enable)
		self.servo = Servo(self.inputServo, 4)
		self.lights = Led(self.inputLed)

	def drive_forward(self, speed=100):
		self.motor1.rotate_clockwise(speed)

	def drive_backward(self, speed=100):
		self.motor1.rotate_counter_clockwise(speed)

	def stop_driving(self):
		self.motor1.stop()

	def go_left(self):
		self.servo.turn(0)

	def go_right(self):
		self.servo.turn(180)

	def go_straight(self):
		self.servo.turn(68)

	def turn_on_lights(self):
		self.lights.on()

	def turn_off_lights(self):
		self.lights.off()

	def turn(self, angle):
		self.servo.turn(angle)
		self.current_angle = angle
