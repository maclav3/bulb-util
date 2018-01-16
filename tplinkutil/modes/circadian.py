import time

import astropy as astropy
from numpy import sin

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


# Disclaimer from the author - I have limited knowledge in Astronomy, so what I'm doing is probably terribly wrong
# Also, there might be code out there that does all this, but I wanted to calculate this myself, for teh kicks
class Sun:
    """Calculates the current position of the sun in the sky"""

    # https://en.wikipedia.org/wiki/Sunrise_equation#Complete_calculation_on_Earth
    def __init__(self, latitude, longitude):
        self._lat = latitude
        self._long = longitude
        self._t = time.time()

    @property
    def _julian_date(self) -> float:
        """Returns the julian date corresponding to the moment in time"""
        return astropy.time.Time(self._t, format='unix').jd

    @property
    def _julian_day(self) -> float:
        """Returns the current Julian Day, according to the Wikipedia article"""
        return self._julian_date - 2451545.0 + 0.0008

    @property
    def _mean_solar_noon(self) -> float:
        """Mean solar noon is an approximation of mean solar time at given longitude
        expressed as a Julian day with the day fraction"""
        return self._julian_day - (self._long / 360.0)

    @property
    def _solar_mean_anomaly(self) -> float:
        return (357.5291 + 0.98560028 * self._mean_solar_noon) % 360.0

    @property
    def _equation_of_the_center(self) -> float:
        M = self._solar_mean_anomaly
        return 1.9148 * sin(M) + 0.0200 * sin(2 * M) + 0.0003 * sin(3 * M)

    @property
    def _ecliptic_longitude(self) -> float:
        # omitting the argument of perihelion correction, it is irrelevant within our precision
        return (self._solar_mean_anomaly + self._equation_of_the_center + 180.0 + 102.9372) % 360.0

    @property
    def _solar_transit(self) -> float:
