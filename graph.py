from datetime import datetime
from cost import cost
import dijkstra as d

import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate

res = 30

if __name__ == '__main__':
    start_time = datetime.now()

    g = d.Graph()

    filename = 'data'+str(res)+'.csv'
    with open(filename, 'r') as file:
        count = 0
        for line in file.readlines():
            val = line.split('\t')
            g.add_vertex(count, float(val[1]),float(val[0]),float(val[2]))
            count += 1

    g.add_edge(0, 1, cost(g.get_vertex(0), g.get_vertex(1)))
    for node in xrange(res**2 - 1):
            if node >= res**2 - res:
                g.add_edge(node, node+1, cost(g.get_vertex(node), g.get_vertex(node+1)))
            else:
                g.add_edge(node, node + res, cost(g.get_vertex(node), g.get_vertex(node + res)))
                if node % res != (res-1):
                    g.add_edge(node, node + 1, cost(g.get_vertex(node), g.get_vertex(node + 1)))

    # for v in g:
    #     print v

    start = round(res/2)
    stop = round(res**2 - res/2-5)

    origin = g.get_vertex(start)
    target = g.get_vertex(stop)

    d.dijkstra(g, g.get_vertex(start))
    path = [target.get_id()]
    d.shortest(target, path)
    print 'The shortest path : %s' % (path[::-1])
    print 'total cost: ' + str(target.distance)

    # for v in g:
    #     print v

    end_time = datetime.now()
    print end_time - start_time

    x = []
    y = []
    z = []

    with open(filename, 'r') as file:
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

    zi = rbf(xi, yi)
    xs = [g.get_vertex(v).lon for v in path]
    ys = [g.get_vertex(v).lat for v in path]
    plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
               extent=[x.min(), x.max(), y.min(), y.max()], cmap='terrain')
    plt.plot(xs, ys, marker='o')
    plt.colorbar()

    text = 'path cost: ' + str(target.distance) + '\n' \
           + 'start: (' + str(round(origin.lat, 3)) + ', ' + str(round(origin.lon, 3)) + ')' + '\n' \
           + 'end: (' + str(round(target.lat, 3)) + ', ' + str(round(target.lon, 3)) + ')' + '\n' \
           + 'path steps: ' + str(len(path))
    plt.suptitle(text, fontsize=14, fontweight='bold')

    plt.show()

