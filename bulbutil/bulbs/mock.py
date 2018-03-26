import colorsys
import time
from tkinter import Frame, Tk, Label, X, PhotoImage
from typing import Tuple, Callable, Any

import webcolors as webcolors

from bulbutil.bulbs import Bulb


def _update_tkinter(f) -> Callable:
    def wrapper(*args) -> Any:
        self = args[0]
        result = f(*args)
        self.update()
        return result

    return wrapper


class MockBulb(Bulb):
    '''This is a mock bulb that shows a GUI dialog representing the current color and brightness.'''

    def __init__(self):
        self._root = None

        # logic-related
        self._brightness = 1.
        self._color = webcolors.rgb_to_hex((255, 255, 255))
        self._on = False

        # tkinter app init
        root = Tk()
        self._frame = Frame(root)
        self.__setup_frame()
        self._frame.pack()
        root.update()
        self._root = root

    def update(self):
        self._widget_bulb.config(bg=self._color)
        self._group_brightness.config(text='Brightness: {}'.format(self._brightness))
        state = 'ON' if self._on else 'OFF'
        self._widget_on.config(text='Bulb state is: {}'.format(state))

        if self._root:
            self._root.update()

    def __setup_frame(self):
        bulb_image = PhotoImage(file='../../resources/bulb-384-600.png')
        self._widget_bulb = Label(self._frame, image=bulb_image)
        self._widget_bulb.photo = bulb_image
        self._widget_bulb.pack(fill=X)

        self._widget_on = Label(self._frame, text='Bulb state not set')
        self._widget_on.pack(fill=X)

        self._group_brightness = Label(self._frame, text='Brightness not set')
        self._group_brightness.pack(fill=X)
        self._frame.update()

    @_update_tkinter
    def turn_on(self):
        self._on = True
        try:
            self._color = self._backupcolor
        except AttributeError:
            self._color = '#ffffff'

    @_update_tkinter
    def turn_off(self):
        self._on = False
        self._backupcolor = self._color
        self._color = '#000000'

    @property
    @_update_tkinter
    def rgb(self) -> Tuple[float, float, float]:
        '''Returns the current RGB color of the bulb in [0,1] range'''
        return self._rgb

    @rgb.setter
    @_update_tkinter
    def rgb(self, rgb: Tuple[float, float, float]):
        '''Sets the current RGB color of the bulb. R, G, B have to be in [0,1] range'''
        self._rgb = rgb
        r, g, b = rgb
        self._color = webcolors.rgb_to_hex((int(255 * r), int(255 * g), int(255 * b)))

    @property
    def brightness(self) -> float:
        '''Returns the current brightness value of the bulb, as a floating point value in [0,1] range'''
        return self._brightness

    @brightness.setter
    @_update_tkinter
    def brightness(self, brightness: float):
        '''Sets the current brightness value of the bulb, as a floating point value in [0,1] range'''
        self._brightness = brightness
        r, g, b = self.rgb
        h, s, _ = colorsys.rgb_to_hsv(r, g, b)
        v = brightness
        self.rgb = colorsys.hsv_to_rgb(h, s, v)


if __name__ == '__main__':
    bulb = MockBulb()
    time.sleep(3)
    bulb.turn_on()
    time.sleep(2)
    bulb.rgb = (1, 0, 0)
    time.sleep(0.5)
    bulb.rgb = (0, 1, 0)
    time.sleep(2)
    bulb.brightness = 0.5
    time.sleep(2)
    bulb.brightness = 0.8
    bulb.rgb = (0.3, 0.5, 0.2)
    time.sleep(4)
    bulb.turn_off()
    time.sleep(3)
