from abc import ABC, abstractmethod
from typing import Tuple


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

    @abstractmethod
    @property
    def rgb(self) -> Tuple[int, int, int]:
        '''Returns the current RGB color of the bulb in [0,255] range'''
        return NotImplemented

    @abstractmethod
    @rgb.setter
    def rgb(self, rgb: Tuple[int, int, int]):
        '''Sets the current RGB color of the bulb. R, G, B have to be in [0,255] range'''
        return NotImplemented

    @abstractmethod
    @property
    def brightness(self) -> float:
        '''Returns the current brightness value of the bulb, as a floating point value in [0,1] range'''
        return NotImplemented

    @abstractmethod
    @brightness.setter
    def brightness(self, value: float):
        '''Sets the current brightness value of the bulb, as a floating point value in [0,1] range'''
        pass

    @property
    def temperature(self):
        return

    @temperature.setter
    def temperature(self, value):
        pass
