import os
import tempfile
import logging

from ibutton import IButton;

class Button(IButton):
    def __init__(self, button_pin):
        IButton.__init__(self)
        self.logger = logging.getLogger("sim_btn")
        self.button_pin = button_pin
        self.path = os.path.join(tempfile.gettempdir(), str(self.button_pin))

    def isPressed(self):
        self.logger.debug("Checking for button: %d (%s)" % (self.button_pin, self.path))
        return os.path.exists(self.path)

    def __str__(self):
        return "b%s" % (str(self.button_pin))
