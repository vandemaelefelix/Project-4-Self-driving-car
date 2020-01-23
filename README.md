**SELF DRIVING CAR**
====================

**By Felix Vandemaele**

**Installation Manual**

![][1]

**Contents** {#contents .TOC-Heading}
============

[**SELF DRIVING CAR** 1]

[Utilities: 3]

[Materials 3]

[Software 3]

[Setup Raspberry Pi 4]

[Hardware 4]

[Enabling Hardware 7]

[Installing Code 7]

[Installing Python Packages 7]

[Update Raspberry Pi 7]

[Installing OpenCV 8]

[Installing TensorFlow 8]

[Install PiCamera 8]

[Install Numpy 8]

[Capturing Data 9]

[Training Model 10]

[Installing Jupyter Lab 10]

[Installing Tensorflow 10]

[Installing Keras 10]

[Start Driving 11]

Utilities:
----------

### Materials

-   RC-car

-   Raspberry Pi 3B+

-   Micro-SD card min. 8GB

-   Micro-SD card reader

-   Power bank min. output of 2A

-   Mini breadboard x2

-   Micro USB cable

-   Jumper wires

-   Servo motor

-   Blue painters' tape

-   MCP 3008

-   L293D DC controller

-   Pi camera v2

-   Some type of glue, I used a glue gun

-   Screwdrivers

-   PVC plate or cardboard could work as well

-   Ethernet cable

-   Potentiometer 10K

-   Resistor 220Ω

-   Clean Raspbian image

-   Soldering iron

### Software

-   Visual Studio Code (or other editor with remote connect function)

-   Putty

-   WinSCP

-   Win32DiskImager

Setup Raspberry Pi
------------------

> For this installation manual I assume that you have a clean install of Raspbian installed on your Raspberry Pi and that you have some basic knowledge of Linux commands and Raspberry Pi. If you don't know how to install your Raspberry Pi, first complete the following document.
>
> 'Preparing your Raspberry Pi V1.docx'

Hardware
--------

> Connect everything to your Raspberry Pi using the following scheme.
>
> ![][2]
>
> The car came with a DC motor for driving and another DC motor for steering. The problem of steering with a DC motor is that you can only steer left or right, but no angle in between. To steer multiple angles, you'll need to replace the DC motor with a servo motor. The steering mechanism is different for every RC-car, so you'll have to be creative to fit the servo. In the picture below you can see how I did it in my car.
>
> ![][3]
>
> Most RC cars use a standard DC motor to drive. Desolder the wires and connect them to the breadboard. The motor uses the regular 4.5V battery that came with the car. Most standard DC motors can handle up to 9V. This will give it more torque but will also generate some heat.
>
> My RC-car already has headlights, so I connected them with the Raspberry Pi as well. I used a resistor, so they won't burn out.
>
> Connect the flat cable of the Pi Camera to the bracket on the Raspberry Pi. Just like on the picture below.
>
> ![Image result for Pi camera v2 in raspberry pi]
>
> I mounted the Pi Camera on a piece of PVC board and hot glued it to the front of the car.
>
> ***Make sure it's very sturdy, because you don't want the camera angle to change at any time. This could affect the performance of your car by a lot!!***
>
> ![][4]
>
> When everything is connected you can stuff it all inside the car. I used a hot glue gun and pieces of PVC board to make sure everything is secured (I think cardboard could do the job as well, but PVC board is a bit sturdier).
>
> ![][5]

Enabling Hardware
-----------------

> To use the Pi Camera and the potentiometer, you must enable some settings.
>
> sudo raspi-config
>
> ![][6]
>
> Under 'Interfacing Options' enable 'Camera' and 'SPI'.
>
> Select 'Finish' and reboot the pi.

Installing Code
---------------

> Clone the code from github into the user folder.
>
> git clone url

Installing Python Packages
--------------------------

> ***You can try to install the newest version of each package, but these versions worked for me so I advise you to use them.***

### Update Raspberry Pi

> Begin with updating your Raspberry Pi so you have all the latest packages available.
>
> sudo apt update
>
> sudo apt upgrade

### Installing OpenCV

> ***!! The latest version of OpenCV doesn't work on Raspberry Pi so you'll have to install an older version !!***
>
> pip3 install opencv-python==3.4.6.27
>
> pip3 install opencv-contrib-python==3.4.3.18

### Installing TensorFlow

> ***!! The latest version of Tensorflow doesn't work on Raspberry Pi so you'll again have to install an older version !!***
>
> pip3 install tensorflow==1.14.0

### Install PiCamera

> pip3 install picamera==1.13

### Install Numpy

> pip3 install numpy==1.16.2

Capturing Data
--------------

> There are several ways to collect data. I mounted a potentiometer on my car to drive it manually. While driving, the camera takes pictures (size of pictures is 640 x 480) and saves them to a data folder.
>
> ![][7]
>
> Depending on how robust you want the model to be, you can collect more and more data. I have about 3000 pictures. They're all taken on one track so it could work on other tracks as well, but not as good as on the original.
>
> To start the 'capture\_data.py' script, type:
>
> cd code/
>
> python3 capture\_data.py -p
>
> When you have enough images, you can transfer them to your computer to train the model.

![][8]

Training Model
--------------

> We'll train the model on our PC because Raspberry Pi isn't strong enough to handle such heavy tasks.
>
> Before training you'll have to install several pip packages.

### Installing Jupyter Lab

> pip3 install jupyterlab

### Installing Tensorflow

> pip3 install tensorflow==2.1.0

### Installing Keras

> pip3 install Keras==2.3.1
>
> In the GitHub repository under 'neural\_network' there is a Jupyter Notebook with the code to train your model.
>
> Inside the Jupyter Notebook, there is a path that refers to a data folder. Edit this path so it leads to the data you just collected.
>
> ![][9]
>
> After training you can save the model as tflite file.
>
> ![][10]
>
> When the model is converted, you can upload it to the Raspberry Pi using WinSCP.

Start Driving
-------------

> You're all done now. The Raspberry Pi is completely setup. Follow the instructions in the user manual to start the car.

  [1]: media/image1.png {width="4.858333333333333in" height="4.858333333333333in"}
  [**SELF DRIVING CAR** 1]: #self-driving-car
  [Utilities: 3]: #utilities
  [Materials 3]: #materials
  [Software 3]: #software
  [Setup Raspberry Pi 4]: #setup-raspberry-pi
  [Hardware 4]: #hardware
  [Enabling Hardware 7]: #enabling-hardware
  [Installing Code 7]: #installing-code
  [Installing Python Packages 7]: #installing-python-packages
  [Update Raspberry Pi 7]: #update-raspberry-pi
  [Installing OpenCV 8]: #installing-opencv
  [Installing TensorFlow 8]: #installing-tensorflow
  [Install PiCamera 8]: #install-picamera
  [Install Numpy 8]: #install-numpy
  [Capturing Data 9]: #capturing-data
  [Training Model 10]: #training-model
  [Installing Jupyter Lab 10]: #installing-jupyter-lab
  [Installing Tensorflow 10]: #installing-tensorflow-1
  [Installing Keras 10]: #installing-keras
  [Start Driving 11]: #start-driving
  [2]: media/image2.png {width="6.531944444444444in" height="4.745138888888889in"}
  [3]: media/image3.png {width="5.6875in" height="2.606720253718285in"}
  [Image result for Pi camera v2 in raspberry pi]: media/image4.jpeg {width="3.7356430446194224in" height="3.1041666666666665in"}
  [4]: media/image5.png {width="2.5694444444444446in" height="3.1934897200349956in"}
  [5]: media/image6.png {width="5.848295056867891in" height="2.6804155730533683in"}
  [6]: media/image7.png {width="5.601896325459317in" height="2.9706846019247592in"}
  [7]: media/image8.png {width="4.430555555555555in" height="2.428185695538058in"}
  [8]: media/image9.jpeg {width="2.9027777777777777in" height="2.177237532808399in"}
  [9]: media/image10.png {width="3.0277777777777777in" height="3.145488845144357in"}
  [10]: media/image11.png {width="4.968786089238845in" height="1.677095363079615in"}
