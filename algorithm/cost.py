from geopy.distance import vincenty

# path cost parameters
WALK_COST = 1
CLIMBING_COST = 100

def print_v(v):
    print '\t' + 'id ' + str(v.id) + ' lat ' + str(v.lat) + ' lon ' + str(v.lon) + ' ele ' + str(v.ele)


def cost(start_lon, start_lat, start_ele, stop_lon, stop_lat, stop_ele):
    horizontal_dist = vincenty((start_lon, start_lat), (stop_lon, stop_lat)).meters
    # elevation_dist = abs(to.ele - frm.ele)
    elevation_dist = stop_ele - start_ele if (stop_ele - start_ele > 0) else 10

    total_cost = WALK_COST * round(horizontal_dist) + elevation_dist * CLIMBING_COST
    # print str(frm.id), '->', str(to.id), ': horizontal: ', round(horizontal_dist), 'elevation: ', elevation_dist, 'total: ', total_cost
    # print_v(frm)
    # print_v(to)
    return total_cost
