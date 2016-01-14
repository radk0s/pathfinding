from algorithm.graph import graph_path
from algorithm.adaptation import adaptation_path

if __name__ == '__main__':

    res = 30
    start = 880
    stop = 138

    dijkstra_path = graph_path(start, stop, res)
    print dijkstra_path
    adaptation_path('config.yml')