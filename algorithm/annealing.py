from __future__ import print_function
import math
import random
from simanneal import Annealer

class TSP(Annealer):

    def __init__(self, state, elevationFn, costFn):
        self.elevationFn = elevationFn
        self.costFn = costFn
        super(TSP, self).__init__(state)  # important!

    def move(self):
        """Swaps two cities in the route."""
        # todo do adaptation here
        # 1 initial N steps do swap beetween two points (if we have random points at start)
        # 2 then every M steps move some points for random direction and distance for local cost reduction
        # 3 then every M steps split some parts of path considering cost reduction
        # 4 back to 2
        # 5 stop divisions if we have specific number of parts
        a = random.randint(1, len(self.state) - 2)
        b = random.randint(1, len(self.state) - 2)
        self.state[a], self.state[b] = self.state[b], self.state[a]

    def energy(self):
        """Calculates the length of the route."""
        return self.costFn(self.state, self.elevationFn)
