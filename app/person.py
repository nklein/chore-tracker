import time
import logging
from enum import Enum
from ibutton import ButtonState
from schedule import Schedule

class PersonState(Enum):
    IDLE = 1
    TIME_FOR_CHORES = 2
    REALLY_TIME_FOR_CHORES = 3
    DOING_CHORES = 4

class Person:
    SECONDS_UNTIL_REALLY_TIME = 45 * Schedule.SECONDS_PER_MINUTE

    def __init__(self, name, button, lightControl, schedule):
        self.logger = logging.getLogger(name)
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

        if self.state == PersonState.IDLE and self.isTimeToStartChores():
            self.setState(PersonState.TIME_FOR_CHORES)
        elif self.state == PersonState.TIME_FOR_CHORES and self.isReallyTimeToStartChores():
            self.setState(PersonState.REALLY_TIME_FOR_CHORES)

        self.lightControl.tick()
        pass

    def setState(self, state):
        if self.state != state:
            self.logger.info("State changed %s -> %s" % ( self.state, state))
            self.state = state
            self.stateStarted = time.time()
            if self.state == PersonState.IDLE:
                self.nextScheduledTime = self.schedule.getNextScheduledTime(self.stateStarted)
                if self.nextScheduledTime == None:
                    self.logger.info("No next chore time")
                else:
                    self.logger.info("Next chore time is %s" % ( time.ctime(self.nextScheduledTime) ))
                self.lightControl.off()
            elif self.state == PersonState.TIME_FOR_CHORES:
                self.lightControl.pulse(1)
            elif self.state == PersonState.REALLY_TIME_FOR_CHORES:
                self.lightControl.pulse(3)
            else:
                self.lightControl.on()
        pass


    def isTimeToStartChores(self):
        return self.nextScheduledTime != None and self.nextScheduledTime <= time.time()

    def isReallyTimeToStartChores(self):
        delta = time.time() - self.stateStarted
        self.logger.debug("delta is: %d vs %d" % (delta, Person.SECONDS_UNTIL_REALLY_TIME))
        return Person.SECONDS_UNTIL_REALLY_TIME <= delta
