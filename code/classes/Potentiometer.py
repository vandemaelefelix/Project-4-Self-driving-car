import RPi.GPIO as GPIO

class Potentiometer:
    def __init__(self,_clk, _miso, _mosi, _cs, _pot_adc):
        self.clk = _clk
        self.miso = _miso
        self.mosi = _mosi
        self.cs = _cs
        self.pot_adc = _pot_adc

        GPIO.setup([self.mosi, self.clk, self.cs], GPIO.OUT)
        GPIO.setup(self.miso, GPIO.IN)

    def read_value(self):
        if ((self.pot_adc > 7) or (self.pot_adc < 0)):
            return -1
        GPIO.output(self.cs, True)

        GPIO.output(self.clk, False)  # start clock low
        GPIO.output(self.cs, False)     # bring CS low

        commandout = self.pot_adc
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
            if (commandout & 0x80):
                GPIO.output(self.mosi, True)
            else:
                    GPIO.output(self.mosi, False)
            commandout <<= 1
            GPIO.output(self.clk, True)
            GPIO.output(self.clk, False)
        
        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
            GPIO.output(self.clk, True)
            GPIO.output(self.clk, False)
            adcout <<= 1
            if (GPIO.input(self.miso)):
                adcout |= 0x1
        
        GPIO.output(self.cs, True)

        adcout >>= 1	# first bit is 'null' so drop it
        return round(adcout / 1024.0, 2)