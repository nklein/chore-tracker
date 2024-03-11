import time

from iledbutton import ILEDButton
from ibutton import ButtonState

# Class for testing buttons
class ButtonTester:
    def __init__(self, factory):
        self.factory = factory
        self.delay = 1
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
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> BUTTON PRESSED")
                elif state == ButtonState.RELEASING:
                    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< BUTTON RELEASED")
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
    print("About to loop cycling buttons")
    while True:
        tester.testButtons()
