import abc


class Mode(abc.ABC):
    CIRCADIAN = 'circadian'
    MUSIC = 'music'
    JOYSTICK = 'joystick'

    def __init__(self, mode, timestep: float):
        self.mode = mode
        self.timestep = timestep

    @property
    @abc.abstractmethod
    def name(self):
        """Returns the mode's name"""
        return NotImplemented

    @abc.abstractmethod
    def __call__(self):
        """This is called on each tick and is intended to change the lighting according to the mode's internal logic"""
        return NotImplemented
