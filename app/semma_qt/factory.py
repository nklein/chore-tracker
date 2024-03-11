from iledbuttonfactory import ILEDButtonFactory

from .ledbutton import LEDButton

import board
from adafruit_seesaw.seesaw import Seesaw

class LEDButtonFactory(ILEDButtonFactory):
    def __init__(self, addr=0x3A):
        self.i2c = board.I2C()
        self.arcade_qt = Seesaw(self.i2c, addr)

    def makeLEDButton(self, led_pin, button_pin):
        return LEDButton(self.arcade_qt, led_pin, button_pin)
