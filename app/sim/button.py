import os
import tempfile

from ibutton import IButton;

class Button(IButton):
    def __init__(self, button_pin):
        IButton.__init__(self)
        self.button_pin = button_pin
        self.path = os.path.join(tempfile.gettempdir(), str(self.button_pin))

    def isPressed(self):
        print("### checking if button %d is pressed (%s)" % (self.button_pin, self.path))
        return os.path.exists(self.path)
