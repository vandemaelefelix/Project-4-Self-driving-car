import tensorflow as tf
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import cv2 as cv
import numpy as np
import logging
from classes.Car import Car
from classes.Potentiometer import Potentiometer
from threading import Thread
import argparse

def predict_angle(image):
    input_data = np.reshape(cv.resize(preprocess(image), (200,66), interpolation=cv.INTER_CUBIC).astype('float32'), (1, 66, 200, 1))
    
    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    return float(output_data[0][0])

def preprocess(image):
    init_height, init_width, _ = image.shape
    YUV_image = cv.cvtColor(image, cv.COLOR_RGB2YUV_I420)
    YUV_height, YUV_width = YUV_image.shape
    process_height = int((YUV_height - init_height) / 2)
    YUV_image = YUV_image[init_height + int(process_height / 2):init_height +
                          process_height, 0:int(init_width / 2)]
    canny_image = cv.Canny(YUV_image, 10, 60)
    
    return canny_image

def main():
    print('running')
    last_value = 0
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        try: 
            angle = predict_angle(frame.array)
            if angle > 100 or angle < 50:
                if (100 - speed) <= 10:
                    rc_car.drive_forward(speed+10)
            else:
                rc_car.drive_forward(speed)
            rc_car.turn(angle)
        except Exception as e:
            logging.error(e)

        rawCapture.truncate(0)

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description='RC car made by Felix Vandemaele.')
        parser.add_argument("-r", default=(640, 480), nargs='+', help="Set's the resolution of the camera.")
        parser.add_argument("-l", action="store_true", help="Enables the headlights.")
        parser.add_argument("-s", default=60, help="Sets the speed of the car in straight lines. In corners, the car wil speed up to have enough momentum.")
        parser.add_argument("-f", default=32, help="Sets the amount of frames per second.")
        args = parser.parse_args()

        print('Starting tensorflow...')
        # Load TFLite model and allocate tensors.
        interpreter = tf.lite.Interpreter(model_path="./model/nvidia_model_v7.tflite")
        interpreter.allocate_tensors()

        # Get input and output tensors.
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        print('Starting camera...')
        resolution = (int(args.r[0]), int(args.r[1]))
        camera = PiCamera()
        camera.resolution = resolution
        camera.framerate = args.f
        rawCapture = PiRGBArray(camera, size=resolution)

        print('Starting rc car...')
        GPIO.setmode(GPIO.BCM)
        rc_car = Car(2, 3, 4, 17, 27)

        if args.l:
            rc_car.turn_on_lights()
        else:
            rc_car.turn_off_lights()

        speed = int(args.s)
        time.sleep(0.1)
        rc_car.drive_forward(speed)

        main()
    except Exception as e:  
        logging.error(e)
    finally:
        GPIO.cleanup()