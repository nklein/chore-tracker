import os
import tempfile

from ibutton import IButton;

class Button(IButton):
    def __init__(self, button_pin):
        IButton.__init__(self)
        self.button_pin = button_pin
        self.path = os.path.join(tempfile.gettempdir(), str(self.button_pin))

    def isPressed(self):
        return os.path.exists(self.path)
