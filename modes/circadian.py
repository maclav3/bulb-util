import geoip

from modes import Mode, logger


class Circadian(Mode):
    def __init__(self, latitude=None, longitude=None):
        self.latitude = latitude
        self.longitude = longitude
        if not latitude or not longitude:
            location = geoip.geolite2.lookup_mine()

            if not latitude:
                self.latitude = location.location[0]
                logger.info('Latitude not supplied, setting latitude to %f from geoip data' % (self.latitude))
            if not longitude:
                self.longitude = location.location[1]
                logger.info('Longitude not supplied, setting longitude to %f from geoip data' % (self.longitude))

        def getname(self):
            return 'circadian'
