import time

from config import Config
from lightcontrol import LightControl
from person import Person
from schedule import Schedule

import test.buttons as btest

from semma_qt.factory import LEDButtonFactory
from sim.factory import LEDButtonFactory as SimLEDButtonFactory

class Application:
    DELAY = 1

    def __init__(self):
        self.config = Config()
        self.people = dict()

    def setupFactory(self):
        print("Making button factory")
        if self.config.isSimMode():
            print("Simulation mode")
            self.factory = SimLEDButtonFactory()
        else:
            print("Real mode")
            self.factory = LEDButtonFactory()

    def printConfig(self):
        for handle in self.config.getHandles():
            print("===============================")
            print("    handle: %s" % (handle))
            print("      name: %s" % (self.config.getPersonName(handle)))
            print("   led_pin: %s" % (self.config.getPersonLEDPin(handle)))
            print("button_pin: %s" % (self.config.getPersonButtonPin(handle)))
            print("    sunday: %s" % (self.config.getPersonSchedule(handle, Config.SUNDAY)))
            print("    monday: %s" % (self.config.getPersonSchedule(handle, Config.MONDAY)))
            print("   tuesday: %s" % (self.config.getPersonSchedule(handle, Config.TUESDAY)))
            print(" wednesday: %s" % (self.config.getPersonSchedule(handle, Config.WEDNESDAY)))
            print("  thursday: %s" % (self.config.getPersonSchedule(handle, Config.THURSDAY)))
            print("    friday: %s" % (self.config.getPersonSchedule(handle, Config.FRIDAY)))
            print("  saturday: %s" % (self.config.getPersonSchedule(handle, Config.SATURDAY)))
            print("===============================")

    def testButtons(self):
        print("Trying buttons")
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
        print("Reading config file")
        self.config.readConfig()
        self.printConfig()
        self.setupFactory()
        self.createPeople()
        self.mainLoop()
        pass

if __name__ == "__main__":
    app = Application()
    app.main()
