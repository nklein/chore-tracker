import json

class Config:
    SIM_MODE = "sim_mode"

    DEFAULTS = "defaults"
    PEOPLE = "people"
    NAME = "name"
    LED_PIN = "led_pin"
    BUTTON_PIN = "button_pin"

    TIMING = "timing"
    LOOP_DELAY = "loop_delay"
    DEFAULT_LOOP_DELAY = 0.01

    SCHEDULE = "schedule"
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

    def __init__(self):
        self.config = dict()
        pass

    def readConfig(self, config = "config.json"):
        with open(config, "r") as file:
            self.config = json.load(file)
        pass

    def printConfig(self):
        print("simulated %s" % (self.isSimMode()))
        print("loop delay = %f" % (self.getLoopDelay()))
        for handle in self.getHandles():
            print("===============================")
            print("    handle: %s" % (handle))
            print("      name: %s" % (self.getPersonName(handle)))
            print("   led_pin: %s" % (self.getPersonLEDPin(handle)))
            print("button_pin: %s" % (self.getPersonButtonPin(handle)))
            print("    sunday: %s" % (self.getPersonSchedule(handle, Config.SUNDAY)))
            print("    monday: %s" % (self.getPersonSchedule(handle, Config.MONDAY)))
            print("   tuesday: %s" % (self.getPersonSchedule(handle, Config.TUESDAY)))
            print(" wednesday: %s" % (self.getPersonSchedule(handle, Config.WEDNESDAY)))
            print("  thursday: %s" % (self.getPersonSchedule(handle, Config.THURSDAY)))
            print("    friday: %s" % (self.getPersonSchedule(handle, Config.FRIDAY)))
            print("  saturday: %s" % (self.getPersonSchedule(handle, Config.SATURDAY)))
            print("===============================")

    def isSimMode(self):
        return self.config[Config.SIM_MODE]

    def getLoopDelay(self):
        try:
            return self.config[Config.TIMING][Config.LOOP_DELAY];
        except KeyError:
            return DEFAULT_LOOP_DELAY

    def getHandles(self):
        return list(self.config[Config.PEOPLE].keys())

    def getPersonName(self, handle):
        return self.config[Config.PEOPLE][handle][Config.NAME]

    def getPersonLEDPin(self, handle):
        return self.config[Config.PEOPLE][handle][Config.LED_PIN]

    def getPersonButtonPin(self, handle):
        return self.config[Config.PEOPLE][handle][Config.BUTTON_PIN]

    def getPersonSchedule(self, handle, day):
        try:
            return self.config[Config.PEOPLE][handle][Config.SCHEDULE][day]
        except KeyError:
            return self.config[Config.DEFAULTS][Config.SCHEDULE][day]
