import colorsys
from typing import Tuple

from pyHS100 import Discover, SmartBulb

from bulbutil.bulbs import Bulb, ConstantColorBulbException


class TPLink(Bulb):
    def __init__(self, ip=None):
        if not ip:
            d = Discover()
            devices = d.discover()

            for ip, device in devices.iteritems():
                if isinstance(device, SmartBulb):
                    bulb = device
        else:
            bulb = SmartBulb(ip)

        self._bulb = bulb

    @classmethod
    def _normalize_hsv(cls, hsv: Tuple[[float, int], [float, int], [float, int]]) -> Tuple[float, float, float]:
        '''Converts TPLink's [0-360], [0-100], [0-100] HSV range to colorsys' [0-1],[0-1],[0-1]'''
        h, s, v = hsv
        h = h / 360.0
        s = s / 100.0
        v = v / 100.0
        return h, s, v

    @classmethod
    def _denormalize_hsv(cls, hsv: Tuple[float, float, float]) -> Tuple[int, int, int]:
        '''Converts colorsys' [0-1],[0-1],[0-1] range into TPLink's [0-360],[0-360],[0-360]'''
        h, s, v = hsv
        h = int(h * 360)
        s = int(s * 100)
        v = int(v * 100)
        return h, s, v

    def turn_on(self):
        if self._bulb.is_off:
            self._bulb.turn_on()

    def turn_off(self):
        if self._bulb.is_on:
            self._bulb.turn_off()

    @property
    def rgb(self) -> Tuple[float, float, float]:
        '''Returns the current RGB color of the bulb in [0,1] range'''
        h, s, v = TPLink._normalize_hsv(self._bulb.hsv)
        return colorsys.hsv_to_rgb(h, s, v)

    @rgb.setter
    def rgb(self, rgb: Tuple[float, float, float]):
        '''Sets the current RGB color of the bulb. R, G, B have to be in [0,1] range'''
        if not self._bulb.is_variable_color_temp:
            raise ConstantColorBulbException

        r, g, b = rgb
        hsv = colorsys.rgb_to_hsv(r, g, b)
        hsv = TPLink._denormalize_hsv(hsv)
        self._bulb.hsv = hsv

    @property
    def brightness(self) -> float:
        '''Returns the current brightness value of the bulb, as a floating point value in [0,1] range'''
        return self._bulb.brightness / 100.0

    @brightness.setter
    def brightness(self, brightness: float):
        '''Sets the current brightness value of the bulb, as a floating point value in [0,1] range'''
        self._bulb.brightness = int(brightness * 100)
