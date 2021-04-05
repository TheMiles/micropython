import neopixel
import machine
import time

RED    = (255,   0,   0)
YELLOW = (255, 150,   0)
GREEN  = (  0, 255,   0)
CYAN   = (  0, 255, 255)
BLUE   = (  0,   0, 255)
PURPLE = (180,   0, 255)
BLACK  = (  0,   0,   0)




class Pixels(object):

    def __init__(self, pin, num_pixels):

        self.pin        = machine.Pin(5, machine.Pin.OUT)
        self.num_pixels = num_pixels
        self.pixels     = [BLACK]*self.num_pixels
        self.pixels_out = neopixel.NeoPixel(self.pin, self.num_pixels)
        self.brightness = 5


    def write(self):

        b = float(self.brightness) / 255.0

        for i in range(self.num_pixels):
            self.pixels_out[i] = tuple( int( p * b ) for p in self.pixels[i] )

        self.pixels_out.write()


    def __getitem__(self, key):

        return self.pixels[key]


    def __setitem__(self, key, value):

        self.pixels[key] = value

    def __delitem__(self, key):

        self.pixels[key] = BLACK


    def fill(self, color):

        self.pixels = [color] * self.num_pixels
        self.write()


    def color_chase(self, color, wait=0.2):

        for i in range(self.num_pixels):
            self.pixels[i] = color
            self.write()
            time.sleep(wait)


    def wheel(pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)




    def rainbow_cycle(self, wait=0.01, cycles=10):
        for c in range(cycles):
            for j in range(255):
                for i in range(self.num_pixels):
                    rc_index = (i * 256 // self.num_pixels) + j
                    self.pixels[i] = Pixels.wheel(rc_index & 255)
                self.write()
                time.sleep(wait)



