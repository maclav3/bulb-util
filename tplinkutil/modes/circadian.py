import time
from datetime import datetime, timedelta

import pytz
from pysolar import solar, radiation
from tzlocal import get_localzone

from tplinkutil import logger as log
from tplinkutil.modes import Mode
from tplinkutil.utils.geoip import GeoIP

default_timestep = 60  # seconds


class Circadian(Mode):
    def __init__(self, sun: 'Sun', timestep: float = None):
        Mode.__init__(self, self, timestep=timestep)
        if not self.timestep:
            self.timestep = default_timestep  # seconds
            log.info('Timestep not supplied, setting to the default {}'.format(self.timestep))
        else:
            log.info('Setting timestep to {} as requested'.format(self.timestep))

        self.sun = sun

    @property
    def name(self):
        return Mode.CIRCADIAN

    def __call__(self):
        log.debug('circadian mode action')
        self.sun.dt = datetime.now()


class Sun:
    """Calculates the current position of the sun in the sky"""

    def __init__(self,
                 latitude: float = None,
                 longitude: float = None,
                 dt: [int, datetime, time.struct_time] = None,
                 tz: [pytz.tzfile.DstTzInfo, pytz.tzfile.StaticTzInfo] = None,
                 geoip=GeoIP()
                 ):
        self._lat, self._long = geoip.completeLatLong(latitude, longitude)
        self._tz = tz or get_localzone()
        self._dt = None
        self._dt = self.__getdatetime(dt)

        self._max_altitude = 0.0
        self._max_radiation = 0.0

    def __getdatetime(self, t: [int, datetime, time.struct_time] = None) -> datetime:
        if not t:
            if not self._dt:
                return datetime.now(tz=self._tz)
            return self._dt
        if isinstance(t, int):
            return datetime.fromtimestamp(t, tz=self._tz)
        if isinstance(t, datetime):
            return t
        if isinstance(t, time.struct_time):
            return datetime.fromtimestamp(time.mktime(t), tz=self._tz)

    @property
    def dt(self) -> datetime:
        return self._dt

    @dt.setter
    def dt(self, t: [int, datetime, time.struct_time]):
        previous_dt = self._dt
        self._dt = self.__getdatetime(t)

        # whenever day changes, recalculate the maximum angle and maximum radiance for this day,
        # in order to be able to scale the color temperature/lightness accordingly
        if previous_dt.tzinfo != self._dt.tzinfo or \
                        abs(previous_dt - self._dt).days > 0 or \
                        previous_dt.day != self._dt.day:
            maxalt = 0.0
            maxrad = 0.0

            _dt = self._dt
            _dt = _dt.replace(_dt.year, _dt.month, _dt.day, 0, 0, 0)
            for i in range(240):
                alt = self.altitude(_dt)
                if alt > maxalt:
                    maxalt = alt
                rad = self.radiation(_dt)
                if rad > maxrad:
                    maxrad = rad
                _dt = _dt + timedelta(minutes=10)

            self._max_altitude = maxalt
            self._max_radiation = maxrad

    @dt.deleter
    def dt(self):
        self._dt = None
        self._max_altitude = None
        self._max_radiation = None

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

    @property
    def max_altitude(self):
        """The maximum altitude that the Sun will attain in a given day (based on `dt`). Useful for scaling."""
        return self._max_altitude

    def sun_azimuth(self, t: [int, datetime, time.struct_time] = None) -> float:
        """Calculates the azimuth of the sun, in degrees. This differs from the usual sense of azimuth,
        see http://docs.pysolar.org/en/latest/#estimate-of-clear-sky-radiation for details."""
        dt = self.__getdatetime(t)
        return solar.get_azimuth(self._lat, self._long, dt)

    def azimuth(self, t: [int, datetime, time.struct_time] = None) -> float:
        """Calculates the azimuth of the sun, in degrees. This is in the usual geographical sense of azimuth,
        i.e. north corresponds to 0 degrees."""
        return (self.sun_azimuth(t) + 180.0 + 360.0) % 360.0

    def radiation(self, t: [int, datetime, time.struct_time] = None) -> float:
        """Calculates the clear-sky irradiation in W/m^2"""
        dt = self.__getdatetime(t)
        alt = self.altitude(t)
        return alt > 0 and radiation.get_radiation_direct(dt, alt) or 0.0

    @property
    def max_radiation(self):
        """The maximum radiation that the Sun will attain in a given day (based on `dt`). Useful for scaling."""
        return self._max_radiation


if __name__ == '__main__':
    # demonstration of how Sun works
    tz = get_localzone()
    dt = datetime.now(tz)
    dt = datetime(dt.year, dt.month, dt.day, 0, 0, 0, 0)
    s = Sun()
    print('#Time\tAzimuth\tAltitude\tRadiation\n')
    for i in range(144):
        dt = dt + timedelta(minutes=10)
        t = dt.isoformat()
        s.dt = dt
        alt = s.altitude()
        azm = s.azimuth()
        rad = s.radiation()
        print('{}\t{}\t{}\t{}\n'.format(t, azm, alt, rad))
