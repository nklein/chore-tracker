from enum import Enum
from ibutton import ButtonState

class PersonState(Enum):
    IDLE = 1
    TIME_FOR_CHORES = 2
    REALLY_TIME_FOR_CHORES = 2
    DOING_CHORES = 3

class Person:
    def __init__(self, name, button, lightControl):
        self.name = name
        self.button = button
        self.lightControl = lightControl
        self.state = PersonState.IDLE
        pass

    def tick(self):
        state = self.button.getButtonState()
        if state == ButtonState.PRESSED:
            self.lightControl.disable()
        else:
            self.lightControl.enable()

        if state == ButtonState.RELEASING:
            if self.state == PersonState.IDLE:
                self.setState(PersonState.TIME_FOR_CHORES)
            elif self.state == PersonState.TIME_FOR_CHORES or self.state == PersonState.REALLY_TIME_FOR_CHORES:
                self.setState(PersonState.DOING_CHORES)
            else:
                self.setState(PersonState.IDLE)

        self.lightControl.tick()
        pass

    def setState(self, state):
        if self.state != state:
            self.state = state
            if self.state == PersonState.IDLE:
                self.lightControl.off()
            elif self.state == PersonState.TIME_FOR_CHORES:
                self.lightControl.pulse(1)
            elif self.state == PersonState.REALLY_TIME_FOR_CHORES:
                self.lightControl.pulse(3)
            else:
                self.lightControl.on()
        pass
