import RPi.GPIO as GPIO
from time import sleep
import logging

class DC:
	""" 
	This class lets you control a DC motor with an L293D controller.
	It takes 3 GPIO pins: (1) input for rotating clockwise, (2) input for rotating counterclockwise and (3) input to enbale the DC motor.
	"""

	turning = False

	def __init__(self, input1, input2, enable):
		self.input1 = input1
		self.input2 = input2
		self.enable = enable

		GPIO.setup(self.input1, GPIO.OUT)
		GPIO.setup(self.input2, GPIO.OUT)
		GPIO.setup(self.enable, GPIO.OUT)

		self.pwm=GPIO.PWM(self.enable, 100)

	def rotate_clockwise(self, speed=100, seconds=None):
		""" 
		Spin the DC motor clockwise with a given speed (number between 0 and 100). 
		If a time in seconds is given, the DC motor will stop spinning after the amount of time.
		"""
		try:
			self.pwm.start(0)
			GPIO.output(self.input1, True)
			GPIO.output(self.input2, False)
			self.pwm.ChangeDutyCycle(speed)
			GPIO.output(self.enable, True)

			# If seconds is not set, just keep spinning the DC motor
			if seconds is not None:
				time.sleep(seconds)
				GPIO.output(self.input1, False)
				GPIO.output(self.input2, False)
				GPIO.output(self.enable, False)
				self.pwm.stop()

				self.turning = False
			else:
				self.turning = True
		except Exception as e:
			logging.error(e)

	def rotate_counter_clockwise(self, speed=100, seconds=None):
		""" 
		Spin the DC motor counter clockwise with a given speed (number between 0 and 100).
		If a time in seconds is given, the DC motor will stop spinning after the amount of time.
		"""
		try:
			self.pwm.start(0)
			GPIO.output(self.input1, False)
			GPIO.output(self.input2, True)
			self.pwm.ChangeDutyCycle(speed)
			GPIO.output(self.enable, True)

			if seconds is not None:
				time.sleep(seconds)
				GPIO.output(self.input1, False)
				GPIO.output(self.input2, False)
				GPIO.output(self.enable, False)
				self.pwm.stop()

				self.turning = False
			else:
				self.turning = True
		except Exception as e:
			logging.error(e)

	def stop(self):
		""" 
		Stop spinning th DC motor.
		"""
		try:
			GPIO.output(self.input1, False)
			GPIO.output(self.input2, False)
			GPIO.output(self.enable, False)
			self.pwm.stop()

			self.turning = False
		except Exception as e:
			logging.error(e)