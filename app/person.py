import time
from enum import Enum
from ibutton import ButtonState
from schedule import Schedule

class PersonState(Enum):
    IDLE = 1
    TIME_FOR_CHORES = 2
    REALLY_TIME_FOR_CHORES = 2
    DOING_CHORES = 3

class Person:
    SECONDS_UNTIL_REALLY_TIME = 30 * Schedule.SECONDS_PER_MINUTE

    def __init__(self, name, button, lightControl, schedule):
        self.name = name
        self.button = button
        self.lightControl = lightControl
        self.schedule = schedule
        self.state = None
        self.setState(PersonState.IDLE)
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

        if state == PersonState.IDLE and self.isTimeToStartChores():
            self.setState(PersonState.TIME_FOR_CHORES)
        elif state == PersonState.TIME_FOR_CHORES and self.isReallyTimeToStartChores():
            self.setState(PersonState.REALLY_TIME_FOR_CHORES)

        self.lightControl.tick()
        pass

    def setState(self, state):
        if self.state != state:
            print("[%s] State changed %s -> %s" % ( self.name, self.state, state))
            self.state = state
            self.stateStarted = time.time()
            if self.state == PersonState.IDLE:
                self.nextScheduledTime = self.findNextScheduledTime(self.stateStarted)
                self.lightControl.off()
            elif self.state == PersonState.TIME_FOR_CHORES:
                self.lightControl.pulse(1)
            elif self.state == PersonState.REALLY_TIME_FOR_CHORES:
                self.lightControl.pulse(3)
            else:
                self.lightControl.on()
        pass

    def findNextScheduledTime(self,after):
        offset = self.schedule.getSecondsUntilNextScheduledTime(time.localtime(after))
        if offset == None:
            return None
        else:
            return after + offset

    def isTimeToStartChores(self):
        return self.nextScheduledTime != None and self.nextScheduledTime <= time.time()

    def isReallyTimeToStartChores(self):
        return Person.SECONDS_UNTIL_REALLY_TIME <= time.time() - self.stateStarted
