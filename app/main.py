import time
import getopt
import sys
import logging
import logging.handlers

from config import Config
from lightcontrol import LightControl
from person import Person
from schedule import Schedule

import test.buttons as btest

from stemma_qt.factory import LEDButtonFactory
from sim.factory import LEDButtonFactory as SimLEDButtonFactory

class Application:
    def __init__(self):
        self.config = Config()
        self.people = dict()
        self.configFile = "../etc/config.json"
        self.daemonMode = False
        self.logger = None
        self.loopDelay = 0.01
        pass

    def setupFactory(self):
        self.logger.debug("Making button factory")
        if self.config.isSimMode():
            self.logger.info("Simulation mode")
            self.factory = SimLEDButtonFactory()
        else:
            self.logger.info("Real mode")
            self.factory = LEDButtonFactory()
        return 0

    def testButtons(self):
        self.logger.info("Trying buttons")
        btest.tryButtons(self.factory)
        pass

    def createPeople(self):
        ledbuttons = dict()
        overdueTimeout = self.config.getOverdueTimeout()

        for handle in self.config.getHandles():
            name = self.config.getPersonName(handle)
            ledbuttonName = self.config.getPersonLEDButtonName(handle)
            ledbuttons[ ledbuttonName ] = True
            led_pin = self.config.getPersonLEDPin(handle)
            button_pin = self.config.getPersonButtonPin(handle)
            ledbutton = self.factory.makeLEDButton(led_pin, button_pin)
            lightControl = LightControl(ledbuttonName, ledbutton)
            schedule = self.scheduleForHandle(handle)
            self.people[handle] = Person(name, ledbutton, lightControl, schedule, overdueTimeout)

        if len(ledbuttons.keys()) < len(self.config.getHandles()):
            self.logger.fatal("Fewer buttons (%s) than people (%s)"
                              % (list(ledbuttons.keys()), self.config.getHandles()))
            return 1
        return 0

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
            now = time.time()
            for person in self.people.values():
                person.tick(now)
            time.sleep(self.loopDelay)
        return 0

    def setupLogger(self):
        handlers = []

        if self.daemonMode:
            sysLogHandler = logging.handlers.SysLogHandler(address="/dev/log")
            sysLogHandler.setFormatter(logging.Formatter("%(levelname)8s [%(name)-8s] %(message)s"))
            handlers.append(sysLogHandler)
        else:
            streamLogHandler = logging.StreamHandler()
            streamLogHandler.setFormatter(logging.Formatter("%(asctime)s %(levelname)8s [%(name)-8s] %(message)s"))
            handlers.append(streamLogHandler)

        logging.basicConfig(level=logging.INFO, handlers=handlers)
        self.logger = logging.getLogger("app")
        pass

    def usage(self):
        print("python main.py [--config config-file][--daemon]")
        pass

    def parseArgs(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "c:dh", ["config=", "daemon", "help"])
        except getopt.GetoptError as err:
            print(err)
            self.usage()
            return 2

        for o, a in opts:
            if o in ( "-c", "--config" ):
                self.configFile = a
            elif o in ( "-d", "--daemon" ):
                self.daemonMode = True
            elif o in ( "-h", "--help" ):
                self.usage()
                return 2
            else:
                print( "unhandled option: %s" % (o) )
                return 1
        return 0

    def readConfig(self):
        self.logger.info("Reading config file")
        self.config.readConfig(self.configFile)
        self.config.printConfig()
        return 0

    def setupLocalParameters(self):
        self.loopDelay = self.config.getLoopDelay()
        return 0

    def main(self):
        return (
            self.parseArgs()
            or self.setupLogger()
            or self.readConfig()
            or self.setupLocalParameters()
            or self.setupFactory()
            or self.createPeople()
            or self.mainLoop()
        )

if __name__ == "__main__":
    app = Application()
    sys.exit(app.main())
