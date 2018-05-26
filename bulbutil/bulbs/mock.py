import colorsys
import threading
import time
from os import path
from typing import Tuple

import pygame
import webcolors as webcolors

from bulbutil.bulbs import Bulb


class Pygame:
    '''This is a small pygame app that represents the change of state of the virtual bulb'''

    screen_size = (384, 600)

    event_set_rgb = pygame.USEREVENT + 1

    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(self.screen_size)
        self._done = False
        clock = pygame.time.Clock()
        bulb_image = pygame.image.load(path.join('..', '..', 'resources', 'bulb-384-600.png'))

        while not self._done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._done = True
                elif event.type == self.event_set_rgb:
                    screen.fill(event.rgb)
            screen.blit(bulb_image, bulb_image.get_rect())
            pygame.display.flip()

            clock.tick(60)

    @classmethod
    def send_rgb_event(cls, rgb: Tuple[int, int, int]):
        pygame.event.post(pygame.event.Event(cls.event_set_rgb, {'rgb': rgb}))

    def __del__(self):
        self._done = True


class MockBulb(Bulb):
    '''This is a mock bulb that shows a GUI dialog representing the current color and brightness.'''

    def __init__(self):
        # logic-related
        self._rgb = (0.0, 0.0, 0.0)
        self._brightness = 1.
        self._color = webcolors.rgb_to_hex((255, 255, 255))
        self._on = False

        print('Creating game')
        self._game_thread = threading.Thread(target=Pygame)
        print('starting game')
        self._game_thread.start()
        print('game started')

    def __del__(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        self._game_thread.join()
        print('cleaned up lol')

    def turn_on(self):
        self._on = True
        try:
            self._color = self._backupcolor
        except AttributeError:
            self._color = '#ffffff'

    def turn_off(self):
        self._on = False
        self._backupcolor = self._color
        self._color = '#000000'

    @property
    def rgb(self) -> Tuple[float, float, float]:
        '''Returns the current RGB color of the bulb in [0,1] range'''
        return self._rgb

    @rgb.setter
    def rgb(self, rgb: Tuple[float, float, float]):
        '''Sets the current RGB color of the bulb. R, G, B have to be in [0,1] range'''
        self._rgb = rgb
        r, g, b = rgb
        r, g, b = (int(255 * r), int(255 * g), int(255 * b))
        self._color = webcolors.rgb_to_hex((r, g, b))

        Pygame.send_rgb_event((r, g, b))

    @property
    def brightness(self) -> float:
        '''Returns the current brightness value of the bulb, as a floating point value in [0,1] range'''
        return self._brightness

    @brightness.setter
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
    del (bulb)
