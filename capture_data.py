from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import cv2 as cv
import numpy as np
from math import degrees, atan
import logging
from classes.Car import Car
from classes.Potentiometer import Potentiometer
from threading import Thread

def run_camera():
    # Starting the PiCamera with a resolution of 640 x 480
    camera = PiCamera()
    camera.resolution = resolution
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=resolution)


    # Give the camera some time to warm up
    time.sleep(0.1)

    # capture frames from the camera
    i=0
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        img = frame.array
        try:
            cv.imwrite("data/%s_%03d_%03d.png" % ("vide126", i, rc_car.current_angle), img)
            i+=1
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(e)

        rawCapture.truncate(0)

def run_potentiometer(rc_car, pot):
    while 1:
        # angle = float(pot.read_value())
        angle = float(pot.read_value() * 180)
        rc_car.turn(angle)
        time.sleep(0.01)

def main():
    thread1 = Thread( target=run_camera) #, args=(rc_car, ) )
    thread1.start()
    if(args.p):
        thread2 = Thread( target=run_potentiometer, args=(rc_car, potentiometer, ) )
        thread2.start()
        thread2.join()
    
    thread1.join()


if __name__ == "__main__":
    try:
        # Setting arguments for script
        import argparse
        parser = argparse.ArgumentParser(description='RC car made by Felix Vandemaele')
        parser.add_argument("-r", default=(640, 480), nargs='+', help="Set's the resolution of the camera.")
        parser.add_argument("-p", action="store_true", help="Enables the potentiometer of the car to steer with.")
        args = parser.parse_args()

        GPIO.setmode(GPIO.BCM)
        rc_car = Car(2, 3, 4, 17, 27)
        potentiometer = Potentiometer(16, 19, 20, 25, 0)  

        print('Starting rc car...')
        resolution = (int(args.r[0]), int(args.r[1]))
        width, height = resolution
        time.sleep(5)
        main()
    except Exception as e:  
        logging.error(e)
    finally:  
        GPIO.cleanup()