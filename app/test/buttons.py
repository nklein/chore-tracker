import time
import logging

from iledbutton import ILEDButton
from ibutton import ButtonState

# Class for testing buttons
class ButtonTester:
    def __init__(self, factory):
        self.logger = logging.getLogger("test_btns")
        self.factory = factory
        self.delay = 0.01
        self.initButtons()

    def initButtons(self):
        self.buttons = []
        self.buttons.append(self.factory.makeLEDButton(12, 18))
        self.buttons.append(self.factory.makeLEDButton(13, 19))
        self.buttons.append(self.factory.makeLEDButton( 0, 20))
        self.buttons.append(self.factory.makeLEDButton( 1,  2))

    def rampIdleButtons(self, start, end, step):
        for cycle in range(start, end, step):
            for button in self.buttons:
                state = button.getButtonState()
                if state == ButtonState.PRESSING:
                    self.logger.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> BUTTON PRESSED %s" % (button))
                elif state == ButtonState.RELEASING:
                    self.logger.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< BUTTON RELEASED %s" % (button))
                elif state == ButtonState.PRESSED:
                    button.setBrightness(0)
                else:
                    button.setBrightness(cycle)
            time.sleep(self.delay)

    def testButtons(self):
        self.rampIdleButtons(0, 65535, 8000)
        self.rampIdleButtons(65535, 0, -8000)

def tryButtons(factory):
    tester = ButtonTester(factory)
    logging.getLogger("test_btns").info("About to loop cycling buttons")
    while True:
        tester.testButtons()
