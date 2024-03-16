import logging

from iled import ILED
from adafruit_seesaw.pwmout import PWMOut

class LED(ILED):
    def __init__(self, arcade_qt, led_pin):
        self.logger = logging.getLogger("led")
        self.logger.info("Creating PWMOut for pin %d" % (led_pin))
        self.led = PWMOut(arcade_qt, led_pin)

    def setBrightness(self, brightness):
        self.led.duty_cycle = brightness
