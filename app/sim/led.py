import logging
from iled import ILED

class LED(ILED):
    def __init__(self, led_pin):
        self.logger = logging.getLogger("sim_led")
        self.led_pin = led_pin
        self.lastBrightness = None

    def setBrightness(self, brightness):
        if brightness != self.lastBrightness:
            self.logger.debug("Setting brightness %s -> %d for led %d"
                              % (self.lastBrightness, brightness, self.led_pin))
            self.lastBrightness = brightness
