
class LightControl:
    MIN_BRIGHTNESS = 2048
    MAX_BRIGHTNESS = 65535
    PULSE_WAVELENGTH = 20

    def __init__(self, led):
        self.led = led
        self.tickCount = 0
        self.speed = 0
        self.brightness = LightControl.MIN_BRIGHTNESS
        self.enable()
        self.off()
        pass

    def enable(self):
        self.enabled = True
        self.__set_light__()
        pass

    def disable(self):
        self.enabled = False
        self.__set_light__()
        pass

    def tick(self):
        self.tickCount += 1
        self.__set_light__()
        pass

    def pulse(self, speed):
        self.speed = speed
        self.tickCount = 0
        self.__set_light__()
        pass

    def on(self):
        self.speed = 0
        self.brightness = LightControl.MAX_BRIGHTNESS
        self.__set_light__()
        pass

    def off(self):
        self.speed = 0
        self.brightness = LightControl.MIN_BRIGHTNESS
        self.__set_light__()
        pass

    def isOn(self):
        return self.speed == 0 and self.brightness > LightControl.MIN_BRIGHTNESS

    def isOff(self):
        return self.speed == 0 and self.brightness < LightControl.MAX_BRIGHTNESS

    def isPulsing(self):
        return self.speed > 0

    def __set_light__(self):
        self.led.setBrightness(self.__get_brightness__())
        pass

    def __get_brightness__(self):
        if self.enabled:
            if self.isPulsing():
                return self.__calc_pulse_brightness__()
            else:
                return self.brightness
        return 0

    def __calc_pulse_brightness__(self):
        distance = ( self.speed * self.tickCount ) % LightControl.PULSE_WAVELENGTH
        lessThanHalfway = ( distance * 2 <= LightControl.PULSE_WAVELENGTH )
        height = distance if lessThanHalfway else ( LightControl.PULSE_WAVELENGTH - distance )
        delta = ( LightControl.MAX_BRIGHTNESS - LightControl.MIN_BRIGHTNESS ) * height * 2
        return round(( delta / LightControl.PULSE_WAVELENGTH ) + LightControl.MIN_BRIGHTNESS)
