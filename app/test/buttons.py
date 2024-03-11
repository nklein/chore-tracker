import time
import board
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.digitalio import DigitalIO
from adafruit_seesaw.pwmout import PWMOut

class Button:
    def __init__(self, arcade_qt, button_pin):
        print("Creating INPUT/Pull-UP button for pin", button_pin)
        self.button = DigitalIO(arcade_qt, button_pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP

    def isPressed(self):
        return self.button.value

class LED:
    def __init__(self, arcade_qt, led_pin):
        print("Creating PWMOut for pin", led_pin)
        self.led = PWMOut(arcade_qt, led_pin)

    def setBrightness(self, brightness):
        self.led.duty_cycle = brightness

class LEDButton(LED, Button):
    def __init__(self, arcade_qt, led_pin, button_pin):
        LED.__init__(self, arcade_qt, led_pin)
        Button.__init__(self, arcade_qt, button_pin)

# Class for testing buttons
class ButtonTester:
    def __init__(self):
        self.i2c = board.I2C()
        self.arcade_qt = Seesaw(self.i2c, addr=0x3A)
        self.initButtons()

    def initButtons(self):
        self.buttons = []
        self.buttons.append(LEDButton(self.arcade_qt, 12, 18))
        self.buttons.append(LEDButton(self.arcade_qt, 13, 19))
        self.buttons.append(LEDButton(self.arcade_qt,  0, 20))
        self.buttons.append(LEDButton(self.arcade_qt,  1,  2))

    def rampIdleButtons(start, end, step):
        for cycle in range(start, end, step):
            for button in self.buttons:
                if button.isPressed():
                    button.setBrightness(cycle)
                else:
                    button.setBrightness(0)

    def testButtons(self):
        rampIdleButtons(0, 65535, 8000)
        rampIdleButtons(65535, 0, -8000)

def tryButtons():
    tester = ButtonTester()
    print("About to loop cycling buttons")
    while True:
        tester.testButtons()
