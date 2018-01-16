import time as t

from astropy.time import Time
from numpy import sin, arcsin, pi, cos, arccos
from tzlocal import get_localzone

from tplinkutil import logger as log
from tplinkutil.modes import Mode
from tplinkutil.utils.geoip import GeoIP


class Circadian(Mode):
    def __init__(self, timestep: float = None, latitude: float = None, longitude: float = None, geoip=GeoIP()):
        Mode.__init__(self, self, timestep=timestep)
        if not self.timestep:
            self.timestep = 60  # seconds

        self.geoip = geoip
        self.latitude, self.longitude = geoip.completeLatLong(latitude, longitude)

    def getname(self):
        return 'circadian'

    def __call__(self):
        log.debug('circadian action')


# Disclaimer from the author - I have limited knowledge in Astronomy, so what I'm doing is probably terribly wrong
# Also, there might be code out there that does all this, but I wanted to calculate this myself, for teh kicks
class Sun:
    """Calculates the current position of the sun in the sky"""

    # https://en.wikipedia.org/wiki/Sunrise_equation#Complete_calculation_on_Earth
    def __init__(self, latitude: float = None, longitude: float = None, timestamp: float = None, geoip=GeoIP()):
        self._lat, self._long = geoip.completeLatLong(latitude, longitude)
        self._t = timestamp or t.time()
        self._tz = get_localzone()

    @property
    def _julian_date(self) -> float:
        """Returns the julian date corresponding to the moment in time"""
        return Time(self._t, format='unix').jd

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
        m = self._solar_mean_anomaly
        return 1.9148 * sin(m) + 0.0200 * sin(2 * m) + 0.0003 * sin(3 * m)

    @property
    def _ecliptic_longitude(self) -> float:
        # omitting the argument of perihelion correction, it is irrelevant within our precision
        return (self._solar_mean_anomaly + self._equation_of_the_center + 180.0 + 102.9372) % 360.0

    @property
    def _solar_transit(self) -> float:
        return 2451545.5 + self._mean_solar_noon + 0.0053 * sin(self._solar_mean_anomaly) - \
               0.0069 * sin(2 * self._ecliptic_longitude)

    @property
    def _declination_of_sun(self) -> float:
        return arcsin(sin(self._ecliptic_longitude) * sin(23.44 * pi / 180.0))

    @property
    def hour_angle(self) -> float:
        numerator = sin(-0.83 * pi / 180.0) - sin(self._lat) * sin(self._declination_of_sun)
        denominator = cos(self._lat) * cos(self._declination_of_sun)

        return arccos(numerator / denominator)

    @property
    def _julian_sunset(self):
        return self._solar_transit + self.hour_angle / (2 * pi)

    @property
    def _julian_sunrise(self):
        return self._solar_transit - self.hour_angle / (2 * pi)

    @property
    def sunset(self):
        return Time(self._julian_sunset, format='jd').unix

    @property
    def sunrise(self):
        return Time(self._julian_sunrise, format='jd').unix


if __name__ == '__main__':
    from datetime import datetime, timedelta

    tz = get_localzone()
    d = datetime.now(tz)
    d = datetime(d.year, d.month, d.day, 0, 0, 0, 0)
    for i in range(23):
        d = d + timedelta(hours=1)
        s = Sun(timestamp=d.timestamp())
        print('Sunrise: ', datetime.fromtimestamp(s.sunrise, tz=tz))
        print('Sunset : ', datetime.fromtimestamp(s.sunset, tz=tz))
        print('')
