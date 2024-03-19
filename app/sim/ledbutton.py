from iledbutton import ILEDButton

from .led import LED
from .button import Button

class LEDButton(LED, Button, ILEDButton):
    def __init__(self, addr, led_pin, button_pin):
        LED.__init__(self, addr, led_pin)
        Button.__init__(self, addr, button_pin)
        self.addr = addr

    def __str__(self):
        return "%s/%s@%x" % (LED.__str__(self), Button.__str__(self), self.addr)
