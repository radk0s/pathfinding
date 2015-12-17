import simplejson
import urllib
import re

BING_KEY = '&key=AnarNEr3GQtYBpm_uOyX3gA7RLiG5fmSjJc923dpSw--bRyQ66ems66JLGdERei5'
BING_BASE_URL = 'http://dev.virtualearth.net/REST/v1/Elevation/List?points='


def getElevation(lat, lon):
    url = BING_BASE_URL + str(lat) + ',' + str(lon) + BING_KEY

    response = str(simplejson.load(urllib.urlopen(url)))

    rx = '.*(elevations\': \[)(\d+).*'
    match = re.match(rx, response)

    return match.group(2) + '.0'

if __name__ == '__main__':

    startLat = 49.15
    startLon = 19.95
    stopLat = 49.241
    stopLon = 20.086

    resolution = 100

    latStep = (stopLat - startLat) / resolution
    lonStep = (stopLon - startLon) / resolution
    counter = 0
    geoArray = []
    points = []
    with open('dataData.csv', 'w') as file:
        for i in xrange(resolution):
            for j in xrange(resolution):
                counter += 1
                lat = startLat + latStep * i
                lon = startLon + lonStep * j
                urlCoords = str(lat) + ',' + str(lon)
                point = getElevation(lat, lon)
                line = str(lon) + '\t' + str(lat) + '\t' + point + '\n'
                print str(counter) + ' ' + line
                file.write(line)

                # with open('dataData.csv', 'w') as file:
                #     for point in points:
                #         file.write('%f\t%f\t%f\n' % (point['lng'], point['lat'], point['elevation']))
