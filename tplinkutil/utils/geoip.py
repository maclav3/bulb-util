import json
from urllib import request


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
