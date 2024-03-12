import json

class Config:
    SIM_MODE = "sim_mode"

    DEFAULTS = "defaults"
    PEOPLE = "people"
    NAME = "name"
    LED_PIN = "led_pin"
    BUTTON_PIN = "button_pin"

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

    def readConfig(self, config = "config.json"):
        with open(config, "r") as file:
            self.config = json.load(file)
            print("Read configuration file")

    def isSimMode(self):
        return self.config[Config.SIM_MODE]

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
