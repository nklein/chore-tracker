from iled import ILED
from adafruit_seesaw.pwmout import PWMOut

class LED(ILED):
    def __init__(self, arcade_qt, led_pin):
        print("Creating PWMOut for pin", led_pin)
        self.led = PWMOut(arcade_qt, led_pin)

    def setBrightness(self, brightness):
        self.led.duty_cycle = brightness
