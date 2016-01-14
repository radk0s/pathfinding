from __future__ import print_function
import math
import random
from simanneal import Annealer

class TSP(Annealer):

    def __init__(self, state, elevationFn, costFn, periodicFactor, min_lon, max_lon, min_lat, max_lat ):
        self.currentTemp = self.Tmax;
        self.periodicFactor = periodicFactor
        self.min_lon = min_lon
        self.max_lon = max_lon
        self.min_lat = min_lat
        self.max_lat = max_lat
        self.lon_diff = max_lon - min_lon
        self.lat_diff = max_lat - min_lat
        self.elevationFn = elevationFn
        self.costFn = costFn
        self.divideMultiplier = 2
        self.currentStep = 0;
        super(TSP, self).__init__(state)  # important!

    def movePoints(self):
        lon_offset = self.lon_diff * (self.currentTemp/self.Tmax)/2
        lat_offset = self.lat_diff * (self.currentTemp/self.Tmax)/2

        pointIndex = random.randint(1, len(self.state) - 2)
        point = self.state[pointIndex]
        new_lon_max = point[0] + lon_offset if point[0] + lon_offset < self.max_lon else self.max_lon
        new_lon_min = point[0] - lon_offset if point[0] - lon_offset > self.min_lon else self.min_lon
        new_lat_max = point[1] + lat_offset if point[1] + lat_offset < self.max_lat else self.max_lat
        new_lat_min = point[1] - lat_offset if point[1] - lat_offset > self.min_lat else self.min_lat

        new_lon = random.uniform(new_lon_min, new_lon_max)
        new_lat = random.uniform(new_lat_min, new_lat_max)
        self.state[pointIndex] = (new_lon, new_lat)

    def swapPoints(self):
        a = random.randint(1, len(self.state) - 2)
        b = random.randint(1, len(self.state) - 2)
        self.state[a], self.state[b] = self.state[b], self.state[a]

    def dividePath(self):
        pointIndex = random.randint(1, len(self.state) - 2)
        start = self.state[pointIndex]
        end = self.state[pointIndex+1]

        diff_x = end[0] - start[0]
        diff_y = end[1] - start[1]
        step_x = diff_x/self.divideMultiplier
        step_y = diff_y/self.divideMultiplier

        for i in range(self.divideMultiplier):
            self.state.insert(pointIndex, (end[0] - step_x * i, end[1] - step_y * i))

    def move(self):
        # todo do adaptation here
        # 1 (first part period)  move some points for random direction and distance
        # 2 (second part period)  swap random points to change order
        # todo 3 (third part period) split some parts of path
        # 4 back to 1
        self.currentStep += 1

        if math.sin(self.currentStep * math.pi) > 0:
            self.movePoints()
        else:
            self.swapPoints()
        # todo add dividePath() to move

    def energy(self):
        return self.costFn(self.state, self.elevationFn)

    def update(self, step, T, E, acceptance, improvement):
        self.currentTemp = T
        print("Improvment: " + str(improvement) + " %")
    pass
