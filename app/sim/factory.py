import board

from .ledbutton import LEDButton
from iledbuttonfactory import ILEDButtonFactory

class LEDButtonFactory(ILEDButtonFactory):
    def __init__(self):
        pass

    def makeLEDButton(self, addr, led_pin, button_pin):
        return LEDButton(addr, led_pin, button_pin)
