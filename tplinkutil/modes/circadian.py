import time
from datetime import datetime, timedelta

from pysolar import solar
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


class Sun:
    """Calculates the current position of the sun in the sky"""

    def __init__(self, latitude: float = None, longitude: float = None, timestamp: float = None, geoip=GeoIP()):
        self._lat, self._long = geoip.completeLatLong(latitude, longitude)
        self._t = timestamp
        self._tz = get_localzone()

    def __getdatetime(self, t: [int, datetime, time.struct_time] = None) -> datetime:
        if not t:
            return datetime.now(tz=self._tz)
        if isinstance(t, int):
            return datetime.fromtimestamp(t, tz=self._tz)
        if isinstance(t, datetime):
            return t
        if isinstance(t, time.struct_time):
            return datetime.fromtimestamp(time.mktime(t), tz=self._tz)

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, value):
        self._t = value

    @t.deleter
    def t(self):
        self._t = None

    @property
    def latitude(self):
        return self._lat

    @latitude.setter
    def latitude(self, value):
        self._lat = value

    @property
    def longitude(self):
        return self._long

    @longitude.setter
    def longitude(self, value):
        self._long = value

    def altitude(self, t: [int, datetime, time.struct_time] = None) -> float:
        """Calculates the altitude of the sun above the horizon, in degrees of angle"""
        dt = self.__getdatetime(t)
        return solar.get_altitude(self._lat, self._long, dt)

    def azimuth(self, t: [int, datetime, time.struct_time] = None) -> float:
        """Calculates the azimuth of the sun, in degrees"""
        dt = self.__getdatetime(t)
        return (solar.get_azimuth(self._lat, self._long, dt) + 360) % 360


if __name__ == '__main__':
    tz = get_localzone()
    d = datetime.now(tz)
    d = datetime(d.year, d.month, d.day, 0, 0, 0, 0)
    s = Sun()
    for i in range(144):
        d = d + timedelta(minutes=10)
        t = d.isoformat()
        alt = s.altitude(d)
        azm = s.azimuth(d)
        print('{}\t{}\t{}\n'.format(t, alt, azm))
