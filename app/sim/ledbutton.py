from iledbutton import ILEDButton

from .led import LED
from .button import Button

class LEDButton(LED, Button, ILEDButton):
    def __init__(self, led_pin, button_pin):
        LED.__init__(self, led_pin)
        Button.__init__(self, button_pin)
