from iledbuttonfactory import ILEDButtonFactory

from .ledbutton import LEDButton

import board
from adafruit_seesaw.seesaw import Seesaw

class LEDButtonFactory(ILEDButtonFactory):

    def __init__(self):
        self.i2c = board.I2C()
        self.instances = dict()

    def makeLEDButton(self, addr, led_pin, button_pin):
        return LEDButton(self.__getArcadeQt(addr), led_pin, button_pin)

    def __getArcadeQt(self, addr):
        instance = None
        try:
            instance = self.instances[addr]
        except KeyError:
            instance = Seesaw(self.i2c, addr)
            self.instances[addr] = instance
        return instance
