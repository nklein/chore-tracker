import time
import logging
import logging.handlers

from config import Config
from lightcontrol import LightControl
from person import Person
from schedule import Schedule

import test.buttons as btest

from semma_qt.factory import LEDButtonFactory
from sim.factory import LEDButtonFactory as SimLEDButtonFactory

class Application:
    DELAY = 0.01

    def __init__(self, config):
        self.config = config
        self.people = dict()
        self.logger = logging.getLogger("app")

    def setupFactory(self):
        self.logger.debug("Making button factory")
        if self.config.isSimMode():
            self.logger.info("Simulation mode")
            self.factory = SimLEDButtonFactory()
        else:
            self.logger.info("Real mode")
            self.factory = LEDButtonFactory()

    def testButtons(self):
        self.logger.info("Trying buttons")
        btest.tryButtons(self.factory)
        pass

    def createPeople(self):
        for handle in self.config.getHandles():
            name = self.config.getPersonName(handle)
            led_pin = self.config.getPersonLEDPin(handle)
            button_pin = self.config.getPersonButtonPin(handle)
            ledbutton = self.factory.makeLEDButton(led_pin, button_pin)
            lightControl = LightControl(ledbutton)
            schedule = self.scheduleForHandle(handle)
            self.people[handle] = Person(name, ledbutton, lightControl, schedule)
        pass

    def scheduleForHandle(self,handle):
        sunday = self.config.getPersonSchedule(handle, Config.SUNDAY)
        monday = self.config.getPersonSchedule(handle, Config.MONDAY)
        tuesday = self.config.getPersonSchedule(handle, Config.TUESDAY)
        wednesday = self.config.getPersonSchedule(handle, Config.WEDNESDAY)
        thursday = self.config.getPersonSchedule(handle, Config.THURSDAY)
        friday = self.config.getPersonSchedule(handle, Config.FRIDAY)
        saturday = self.config.getPersonSchedule(handle, Config.SATURDAY)
        return Schedule(sunday, monday, tuesday, wednesday, thursday, friday, saturday)

    def mainLoop(self):
        while True:
            for person in self.people.values():
                person.tick()
            time.sleep(Application.DELAY)
        pass

    def main(self):
        self.logger.info("Reading config file")
        self.config.printConfig()
        self.setupFactory()
        self.createPeople()
        self.mainLoop()
        pass

if __name__ == "__main__":
    config = Config()
    config.readConfig()

    handlers = []

    streamLogHandler = logging.StreamHandler()
    streamLogHandler.setFormatter(logging.Formatter("%(asctime)s %(levelname)8s [%(name)-8s] %(message)s"))
    handlers.append(streamLogHandler)

    sysLogHandler = logging.handlers.SysLogHandler(address="/dev/log")
    sysLogHandler.setFormatter(logging.Formatter("%(levelname)8s [%(name)-8s] %(message)s"))
    handlers.append(sysLogHandler)

    logging.basicConfig(level=logging.INFO, handlers=handlers)
    app = Application(config)
    app.main()
