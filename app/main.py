from config import Config

import test.buttons as btest

from semma_qt.factory import LEDButtonFactory
from sim.factory import LEDButtonFactory as SimLEDButtonFactory

class Application:
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
        print("Making button factory")
        if self.config.isSimMode():
            print("Simulation mode")
            factory = SimLEDButtonFactory()
        else:
            print("Real mode")
            factory = LEDButtonFactory()
            print("Trying buttons")
        btest.tryButtons(factory)

    def main(self):
        print("Reading config file")
        self.config = Config()
        self.config.readConfig()
        self.printConfig()
        self.testButtons()

if __name__ == "__main__":
    app = Application()
    app.main()
