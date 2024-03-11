from enum import Enum

class ButtonState(Enum):
    PRESSED = 1
    RELEASED = 2
    PRESSING = 3
    RELEASING = 4

class IButton:
    def __init__(self):
        self.currentState = None
        self.previousState = None

    def getButtonState(self):
        self.previousState = self.currentState
        self.currentState = self.isPressed()

        if self.currentState:
            if self.previousState == True:
                return ButtonState.PRESSED
            else:
                return ButtonState.PRESSING
        else:
            if self.previousState != True:
                return ButtonState.RELEASED
            else:
                return ButtonState.RELEASING

    def isPressed(self):
        return False
