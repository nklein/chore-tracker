from iledbutton import ILEDButton

from .led import LED
from .button import Button

class LEDButton(LED, Button, ILEDButton):
    def __init__(self, arcade_qt, led_pin, button_pin):
        LED.__init__(self, arcade_qt, led_pin)
        Button.__init__(self, arcade_qt, button_pin)

    def __str__(self):
        return "%s/%s" % (LED.__str__(self), Button.__str__(self))
