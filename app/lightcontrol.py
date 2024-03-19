import time
import logging

class LightControl:
    MIN_BRIGHTNESS = 2048
    MAX_BRIGHTNESS = 65535
    PULSE_WAVELENGTH = 5

    def __init__(self, name, led):
        self.logger = logging.getLogger("l:%s" % (name))
        self.led = led
        self.cycleStarted = 0
        self.speed = 0
        self.brightness = LightControl.MIN_BRIGHTNESS
        self.enable()
        self.off()
        pass

    def enable(self):
        self.enabled = True
        self.cycleStarted = time.time()
        self.logger.info("Enable %s" % (self.led))
        self.__set_light__(self.cycleStarted)
        pass

    def disable(self):
        self.enabled = False
        self.__set_light__()
        pass

    def tick(self, now):
        self.__set_light__(now)
        pass

    def pulse(self, speed):
        self.cycleStarted = time.time()
        self.speed = speed
        self.__set_light__(self.cycleStarted)
        pass

    def on(self):
        self.speed = 0
        self.brightness = LightControl.MAX_BRIGHTNESS
        self.__set_light__()
        pass

    def off(self):
        self.speed = 0
        self.brightness = 0
        self.__set_light__()
        pass

    def isOn(self):
        return self.speed == 0 and self.brightness > LightControl.MIN_BRIGHTNESS

    def isOff(self):
        return self.speed == 0 and self.brightness < LightControl.MAX_BRIGHTNESS

    def isPulsing(self):
        return self.speed > 0

    def __set_light__(self, now=None):
        self.led.setBrightness(self.__get_brightness__(now))
        pass

    def __get_brightness__(self, now):
        if self.enabled:
            if self.isPulsing():
                return self.__calc_pulse_brightness__(now)
            else:
                return self.brightness
        return 0

    def __calc_pulse_brightness__(self, now):
        self.logger.debug("Calculating pulse brightness for (%f - %f) = %d"
                          % (now, self.cycleStarted, round(now - self.cycleStarted)))
        elapsed = (now - self.cycleStarted) * self.speed / LightControl.PULSE_WAVELENGTH
        portion = elapsed - int(elapsed)
        height = 2 * (portion if (portion <= 0.5) else (1.0 - portion))
        delta = ( LightControl.MAX_BRIGHTNESS - LightControl.MIN_BRIGHTNESS ) * height
        return round(delta) + LightControl.MIN_BRIGHTNESS
