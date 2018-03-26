from abc import ABC, abstractmethod
from typing import Tuple

import color_temp


class ConstantColorBulbException(Exception):
    def __init__(self):
        Exception.__init__(self, "Bulb cannot change color")


class ConstantBrightnessBulbException(Exception):
    def __init__(self):
        Exception.__init__(self, "Bulb cannot change brightness")


class Bulb(ABC):
    @abstractmethod
    def turn_on(self):
        '''Turns on the bulb'''
        return NotImplemented

    @abstractmethod
    def turn_off(self):
        '''Turns off the bulb'''
        return NotImplemented

    @property
    @abstractmethod
    def rgb(self) -> Tuple[int, int, int]:
        '''Returns the current RGB color of the bulb in [0,1] range'''
        return NotImplemented

    @rgb.setter
    @abstractmethod
    def rgb(self, rgb: Tuple[int, int, int]):
        '''Sets the current RGB color of the bulb. R, G, B have to be in [0,1] range'''
        return NotImplemented

    @property
    @abstractmethod
    def brightness(self) -> float:
        '''Returns the current brightness value of the bulb, as a floating point value in [0,1] range'''
        return NotImplemented

    @brightness.setter
    @abstractmethod
    def brightness(self, brightness: float):
        '''Sets the current brightness value of the bulb, as a floating point value in [0,1] range'''
        pass

    @property
    def temperature(self):
        r, g, b = self.rgb
        return color_temp.rgb_to_temperature((r * 255, g * 255, b * 255))

    @temperature.setter
    def temperature(self, temperature: float):
        r, g, b = color_temp.temperature_to_rgb(temperature)
        self.rgb = (r / 255.0, g / 255.0, b / 255.0)
