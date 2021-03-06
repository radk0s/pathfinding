import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate
import random
import copy
import yaml
from datetime import datetime

from cost import cost as costNorm
import annealing


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

    return total_cost


# generate initial solution


# TODO jak punkty sa zdefiniowane w ten sposob (czyt na odwrot (lon,lat) zamiast (lat,lon)) -> 'from geopy.distance import vincenty' bedzie zle przeliczalo odleglosci!

def generateRandomPoints(start, end, x, y, z, randomPoints):
    points = [start, end]
    return points[:1] + zip(random.sample(x, randomPoints), random.sample(y, randomPoints)) + points[1:]

def generatePoints(start, end, parts):
    randomPoints = 0
    points = [start, end]

    diff_x = end[0] - start[0]
    diff_y = end[1] - start[1]
    step_x = diff_x/parts
    step_y = diff_y/parts
    return points[:1] + [(start[0] + step_x * i, start[1] + step_y * i) for i in range(parts)] + points[1:]

def drawPlot(filename, points, x, y, z, mesh, totalCost, steps, elapsed =0):
    xx, yy = zip(*points)
    plt.imshow(mesh, vmin=np.array(z).min(), vmax=np.array(z).max(), origin='lower',
               extent=[np.array(x).min(), np.array(x).max(), np.array(y).min(), np.array(y).max()], cmap='terrain')
    plt.plot(xx, yy, color='red', lw=2)
    plt.colorbar()


    text = 'path cost: ' + str(totalCost) + '\n' + \
           'steps: ' + str(steps) + '\n' +\
           'time: ' + str(elapsed)

    plt.suptitle(text, fontsize=14, fontweight='bold')
    plt.savefig(filename + '.png')
    plt.close()

    # plt.show()



def adaptation_path(configfile, pointsD = None):
    start_time = datetime.now()
    points = copy.deepcopy(pointsD);

    config = None
    with open(configfile, 'r') as stream:
        config = yaml.load(stream)

    steps = None
    print(points)
    if config['steps'] != None:
        steps = int(config['steps'])

    x, y, z = [], [], []


    mesh, getElevation = prepareElevationFunction(config['data_file'], x, y, z)

    if points == None:
        if config['random_points'] == 1:
            points = generateRandomPoints(
                (config['start_lon'], config['start_lat']),
                (config['end_lon'], config['end_lat']),
                x, y, z, int(config['initial_points_count']))
        else:
            points = generatePoints(
                (config['start_lon'], config['start_lat']),
                (config['end_lon'], config['end_lat']),
                int(config['initial_points_count']))


    pathCost = calculateTotalCost(points, getElevation)

    elapsed = datetime.now() - start_time

    drawPlot('initial_path', points, x, y, z, mesh, calculateTotalCost(points, getElevation), 0, elapsed)
    tsp = annealing.TSP(points, getElevation, calculateTotalCost, 200,
                        np.array(x).min(), np.array(x).max(),
                        np.array(y).min(), np.array(y).max()
                    )
    if steps != None:
        tsp.steps = steps;

    tsp.copy_strategy = "slice"
    state, e = tsp.anneal()

    elapsed = datetime.now() - start_time

    drawPlot('optimized_path_' + (str(steps) if steps != None else 'covergence'), state, x, y, z, mesh, calculateTotalCost(state, getElevation), tsp.currentStep, elapsed)

