import abc


class Mode(abc.ABC):
    CIRCADIAN = 'circadian'
    MUSIC = 'music'
    JOYSTICK = 'joystick'

    def __init__(self, mode, timestep: float):
        self.mode = mode
        self.timestep = timestep

    def getname(self):
        return NotImplemented

    name = property(getname, 'The name of the mode')
