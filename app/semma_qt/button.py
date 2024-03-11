from ibutton import IButton;

from adafruit_seesaw.digitalio import DigitalIO

class Button(IButton):
    def __init__(self, arcade_qt, button_pin):
        IButton.__init__(self)
        print("Creating INPUT/Pull-UP button for pin", button_pin)
        self.button = DigitalIO(arcade_qt, button_pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP

    def isPressed(self):
        return self.button.value
