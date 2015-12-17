import simplejson
import urllib

BING_KEY = '&key=AnarNEr3GQtYBpm_uOyX3gA7RLiG5fmSjJc923dpSw--bRyQ66ems66JLGdERei5'
BING_BASE_URL = 'http://dev.virtualearth.net/REST/v1/Elevation/List?points='

if __name__ == '__main__':
    startLat = 49.119087
    startLon = 19.963777
    stopLat = 49.292461
    stopLon = 20.249254

    resolution = 10

    latStep = (stopLat - startLat) / resolution
    lonStep = (stopLon - startLon) / resolution

    geoArray = []
    points = []
    for i in xrange(resolution):
        for j in xrange(resolution):
            coords = urllib.urlencode('%f,%f' % (startLat + latStep * i, startLon + lonStep * j))
            url = BING_BASE_URL + coords + BING_KEY

            print url
