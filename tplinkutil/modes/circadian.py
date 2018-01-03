from tplinkutil import logger
from tplinkutil.modes import Mode
from tplinkutil.utils.geoip import GeoIP


class Circadian(Mode):
    def __init__(self, timestep=None, latitude=None, longitude=None, geoip=GeoIP()):
        Mode.__init__(self, self, timestep=timestep)
        if not self.timestep:
            self.timestep = 60  # seconds
        self.geoip = geoip
        self.latitude = latitude
        self.longitude = longitude
        if not latitude or not longitude:
            location = self.geoip.getLatLong()

            if not latitude:
                self.latitude = location['latitude']
                logger.info('Latitude not supplied, setting latitude to %f from geoip data' % (self.latitude))
            if not longitude:
                self.longitude = location['longitude']
                logger.info('Longitude not supplied, setting longitude to %f from geoip data' % (self.longitude))

    def getname(self):
        return 'circadian'

    def __call__(self):
        logger.debug('circadian action')
