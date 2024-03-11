from iled import ILED

class LED(ILED):
    def __init__(self, led_pin):
        self.led_pin = led_pin

    def setBrightness(self, brightness):
        print("Setting brightness %d for led %d" % (brightness, self.led_pin))
