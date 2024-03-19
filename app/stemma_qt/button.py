import logging

from ibutton import IButton
from digitalio import Direction, Pull
from adafruit_seesaw.digitalio import DigitalIO


class Button(IButton):
    def __init__(self, arcade_qt, button_pin):
        IButton.__init__(self)
        self.logger = logging.getLogger("btn")
        self.logger.info("Creating INPUT/Pull-UP button for pin %d" % (button_pin))
        self.button_pin = button_pin
        self.button = DigitalIO(arcade_qt, button_pin)
        self.button.direction = Direction.INPUT
        self.button.pull = Pull.UP

    def isPressed(self):
        return not self.button.value

    def __str__(self):
        return "b%s" % (str(self.button_pin))
