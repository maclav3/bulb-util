import json
from typing import Tuple
from urllib import request

from bulbutil import logger as log


class GeoIP(object):
    def __init__(self):
        self.url = 'http://freegeoip.net/json'

    def getLatLong(self):
        resp = request.urlopen(self.url)
        jsonBytes = resp.read()
        resp.close()
        location = json.loads(jsonBytes.decode('utf-8'))
        return ({
            'latitude': location['latitude'],
            'longitude': location['longitude']
        })

    def completeLatLong(self, latitude: float = None, longitude: float = None) -> Tuple[float, float]:
        if not latitude or not longitude:
            location = self.getLatLong()

            if not latitude:
                latitude = location['latitude']
                log.info('Latitude not supplied, setting latitude to {} from geoip data'.format(latitude))
            else:
                log.info('Setting latitude to {} as requested'.format(latitude))
            if not longitude:
                longitude = location['longitude']
                log.info('Longitude not supplied, setting longitude to {} from geoip data'.format(longitude))
            else:
                log.info('Setting longitude to {} as requested'.format(longitude))

        return (latitude, longitude)
