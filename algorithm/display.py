import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import scipy.interpolate
from geopy.distance import vincenty
import random
import sys
import yaml

from cost import cost as costNorm

def prepareElevationFunction(file, x, y, z):
    with open(file, 'r') as file:
        for line in file.readlines():
            val = line.split('\t')
            x.append(float(val[0]))
            y.append(float(val[1]))
            z.append(float(val[2]))

        x = np.array(x)
        y = np.array(y)
        z = np.array(z)

    xi, yi = np.linspace(x.min(), x.max(), 100), np.linspace(y.min(), y.max(), 100)
    xi, yi = np.meshgrid(xi, yi)

    rbf = scipy.interpolate.Rbf(x, y, z, function='linear')

    return (rbf(xi, yi), rbf)


def calculateSegmentCost(start, end):
    return cost(start, end)


def calculateTotalCost(path, elevationFn):
    total_cost= 0
    for i in xrange(len(path) - 1):
        total_cost += costNorm(path[i][0], path[i][1], elevationFn(path[i][0], path[i][1]),
                               path[i + 1][0], path[i + 1][1], elevationFn(path[i + 1][0], path[i + 1][1]))
        print total_cost

    return total_cost


# generate initial solution


# TODO jak punkty sa zdefiniowane w ten sposob (czyt na odwrot (lon,lat) zamiast (lat,lon)) -> 'from geopy.distance import vincenty' bedzie zle przeliczalo odleglosci!


def generatePoints(start, end, x, y, z):
    randomPoints = 5
    points = [start, end]
    print start
    return points[:1] + zip(random.sample(x, randomPoints), random.sample(y, randomPoints)) + points[1:]

def drawPlot(points, x, y, z, mesh, totalCost):
    print np.array(y).min()
    xx, yy = zip(*points)
    plt.imshow(mesh, vmin=np.array(z).min(), vmax=np.array(z).max(), origin='lower',
               extent=[np.array(x).min(), np.array(x).max(), np.array(y).min(), np.array(y).max()], cmap='terrain')
    plt.plot(xx, yy, color='red', lw=2, marker='o')
    plt.colorbar()


    text = 'path cost: ' + str(totalCost) + '\n'
    plt.suptitle(text, fontsize=14, fontweight='bold')

    plt.show()



if __name__ == "__main__":
    config = None
    with open(sys.argv[1], 'r') as stream:
        config = yaml.load(stream)

    x, y, z = [], [], []

    mesh, getElevation = prepareElevationFunction(config['data_file'], x, y, z)

    points = generatePoints(
        (config['start_lon'], config['start_lat']),
        (config['end_lon'], config['end_lat']),
        x, y, z)

    pathCost = calculateTotalCost(points, getElevation)

    drawPlot(points, x, y, z, mesh, pathCost)
