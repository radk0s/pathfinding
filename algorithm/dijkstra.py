import sys

class Vertex:
    def __init__(self, node, lat, lon, ele):
        self.id = node

        self.lat = lat
        self.lon = lon
        self.ele = ele

        self.adjacent = {}
        self.distance = sys.maxint
        self.visited = False
        self.previous = None

    def add_neighbor(self, neighbor, weight=1):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.id) + ' lat: ' + str(self.lat) + ' lon: ' + str(self.lon) + ' ele: ' + str(self.ele) + ' adjacent: ' + str(['('+str(x.id)+': '+str(self.get_weight(x))+')' for x in self.adjacent])

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node, lat, lon, ele):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node, lat, lon, ele)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 1):
        if frm not in self.vert_dict:
            print 'There is no such /from/ vertice'
        if to not in self.vert_dict:
            print 'There is no such /to/ vertice'

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous

def shortest(v, path):
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return

import heapq

def dijkstra(aGraph, start):
    print '''Dijkstra's shortest path begin...'''
    start.set_distance(0)

    unvisited_queue = [(v.get_distance(),v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        for next in current.adjacent:
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)

            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)
            #     print 'updated : current = %s next = %s new_dist = %s' \
            #             %(current.get_id(), next.get_id(), next.get_distance())
            # else:
            #     print 'not updated : current = %s next = %s new_dist = %s' \
            #             %(current.get_id(), next.get_id(), next.get_distance())

        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        unvisited_queue = [(v.get_distance(),v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)
    print '''Dijkstra's shortest path done.'''


