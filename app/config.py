import json

class Config:
    SIM_MODE = "sim_mode"

    DEFAULTS = "defaults"

    LEDBUTTONS = "ledbuttons"
    LED_PIN = "led_pin"
    BUTTON_PIN = "button_pin"

    PEOPLE = "people"
    NAME = "name"
    LEDBUTTON = "ledbutton"

    TIMING = "timing"
    LOOP_DELAY = "loop_delay"
    OVERDUE_TIMEOUT = "overdue_timeout"
    DEFAULT_LOOP_DELAY = 0.01
    DEFAULT_OVERDUE_TIMEOUT = 2700;

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
        print("overdue timeout = %f" % (self.getOverdueTimeout()))

        for button in self.getLEDButtonNames():
            print("===============================")
            print("    button: %s" % (button))
            print("   led_pin: %s" % (self.getLEDButtonLEDPin(button)))
            print("button_pin: %s" % (self.getLEDButtonButtonPin(button)))
            print("===============================")

        for handle in self.getHandles():
            print("===============================")
            print("    handle: %s" % (handle))
            print("      name: %s" % (self.getPersonName(handle)))
            print(" ledbutton: %s" % (self.getPersonLEDButtonName(handle)))
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

    def getOverdueTimeout(self):
        try:
            return self.config[Config.TIMING][Config.OVERDUE_TIMEOUT];
        except KeyError:
            return DEFAULT_OVERDUE_TIMEOUT

    def getLEDButtonNames(self):
        return list(self.config[Config.LEDBUTTONS].keys())

    def getLEDButtonLEDPin(self, button):
        return self.config[Config.LEDBUTTONS][button][Config.LED_PIN];

    def getLEDButtonButtonPin(self, button):
        return self.config[Config.LEDBUTTONS][button][Config.BUTTON_PIN];

    def getHandles(self):
        return list(self.config[Config.PEOPLE].keys())

    def getPersonName(self, handle):
        return self.config[Config.PEOPLE][handle][Config.NAME]

    def getPersonLEDButtonName(self, handle):
        return self.config[Config.PEOPLE][handle][Config.LEDBUTTON]

    def getPersonLEDPin(self, handle):
        return self.getLEDButtonLEDPin(self.getPersonLEDButtonName(handle))

    def getPersonButtonPin(self, handle):
        return self.getLEDButtonButtonPin(self.getPersonLEDButtonName(handle))

    def getPersonSchedule(self, handle, day):
        try:
            return self.config[Config.PEOPLE][handle][Config.SCHEDULE][day]
        except KeyError:
            return self.config[Config.DEFAULTS][Config.SCHEDULE][day]
