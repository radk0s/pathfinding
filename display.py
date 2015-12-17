import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import scipy.interpolate
from geopy.distance import vincenty
import random

x = []
y = []
z = []

with open('dataData.csv', 'r') as file:
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

# function representing terrain
rbf = scipy.interpolate.Rbf(x, y, z, function='linear')

zi = rbf(xi, yi)


def calculate_cost(path):
    WALK_COST = 1
    CLIMBING_COST = 10
    total_distance = 0
    total_diff = 0
    for i in xrange(len(path) - 1):
        total_distance += vincenty(path[i], path[i + 1]).meters
        elevation1 = rbf(path[i][0], path[i][1])
        elevation2 = rbf(path[i + 1][0], path[i + 1][1])
        elevation_diff = elevation2 - elevation1
        if elevation_diff < 0:
            elevation_diff = 0
        total_diff += elevation_diff

    print 'WALK: ', WALK_COST * total_distance, 'CLIMBING: ', total_diff * CLIMBING_COST
    return WALK_COST * total_distance + total_diff * CLIMBING_COST


# generate initial solution
def generatePoints(start, end):
    randomPoints = 5
    points = [start, end]
    return points[:1] + zip(random.sample(x, randomPoints), random.sample(y, randomPoints)) + points[1:]


start = (19.9, 49.12)
end = (20.0138, 49.1618)
points = generatePoints(start, end)
calculate_cost(points)

iter_max = 10
pop_size = 100
dimensions = 2
c1 = 2
c2 = 2


class Particle:
    pass


particles = []
for i in range(pop_size):
    p = Particle()
    p.params = generatePoints(start, end)
    p.fitness = 0.0
    p.v = 0.0
    particles.append(p)

gbest = particles[0]
while i < iter_max:
    for p in particles:
        fitness = calculate_cost(p.params)
        if fitness < p.fitness:
            p.fitness = fitness
            p.best = p.params

        if fitness < gbest.fitness:
            gbest = p
            # ...
    i += 1

# plot result
xx, yy = zip(*points)
plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
           extent=[x.min(), x.max(), y.min(), y.max()], cmap='terrain')
plt.plot(xx, yy, color='red', lw=2, marker='o')
plt.colorbar()
plt.show()
