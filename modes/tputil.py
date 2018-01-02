#!/usr/bin/python3
import time

from modes import Mode, logger


class TPUtil(object):
    def __init__(self, mode: Mode, timestep: float):
        self.mode = mode
        if not timestep:
            # The timestep in daylight simulation need not be very low, let's set the default to a minute
            timestep = 60  # seconds
        self.timestep = timestep

    def run(self):
        logger.info('Starting TPUtil in mode %s with timestep %f' % (self.mode.getname(), self.timestep))
        # main loop
        while True:
            self.mode()
            logger.debug('Tick')
            time.sleep(self.timestep)
