import abc

import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s:%(pathname)s:%(lineno)d: %(message)s'))

logger = colorlog.getLogger('main')
logger.setLevel('DEBUG')
logger.addHandler(handler)


class Mode(abc.ABCMeta):
    CIRCADIAN = 'circadian'
    MUSIC = 'music'
    JOYSTICK = 'joystick'

    def getname(self):
        return NotImplemented

    name = property(getname, 'The name of the mode')
