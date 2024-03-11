from ibutton import IButton;

class Button(IButton):
    def __init__(self, button_pin):
        self.button_pin = button_pin

    def isPressed(self):
        print("### checking if button %d is pressed" % (self.button_pin))
        return False
