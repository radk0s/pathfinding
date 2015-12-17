import simplejson
import urllib

# http://matplotlib.org/examples/pylab_examples/pcolor_demo.html
# http://docs.scipy.org/doc/scipy-0.16.0/reference/generated/scipy.interpolate.griddata.html

ELEVATION_BASE_URL = 'https://maps.googleapis.com/maps/api/elevation/json?key=AIzaSyD2mGMrMAGeyASiBj8NT8eVQYfR2l7nZJk'
BING_KEY = '&key=AnarNEr3GQtYBpm_uOyX3gA7RLiG5fmSjJc923dpSw--bRyQ66ems66JLGdERei5'
BING_BASE_URL = 'http://dev.virtualearth.net/REST/v1/Elevation/List?points='


def getElevation(path, **elvtn_args):
    elvtn_args.update({
        'locations': path
    })
    url = BING_BASE_URL + urllib.urlencode(elvtn_args) + BING_KEY

    response = simplejson.load(urllib.urlopen(url))
    elevationArray = []

    for resultset in response['results']:
        elevationArray.append({
            'lat': resultset['location']['lat'],
            'lng': resultset['location']['lng'],
            'elevation': resultset['elevation'],
            'resolution': resultset['resolution']
        })

    return elevationArray


if __name__ == '__main__':

    startLat = 49.119087
    startLon = 19.963777
    stopLat = 49.292461
    stopLon = 20.249254

    resolution = 30

    latStep = (stopLat - startLat) / resolution
    lonStep = (stopLon - startLon) / resolution

    geoArray = []
    points = []
    for i in xrange(resolution):
        for j in xrange(resolution):
            points += getElevation('%f,%f' % (startLat + latStep * i, startLon + lonStep * j))

    with open('data.csv', 'w') as file:
        for point in points:
            file.write('%f\t%f\t%f\t%f\n' % (point['lng'], point['lat'], point['elevation'], point['resolution']))
