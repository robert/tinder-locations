import math
import random

DEFAULT_DPS = 10

class DistanceMarker:

    def __init__(self, location, distance, precision):
        self.location = location
        self.distance = distance
        self.precision = precision

class DistanceMarkerSet:

    def __init__(self, distance_markers, initial_loc=None):
        self.distance_markers = distance_markers
        self.initial_loc = initial_loc

    def distances(self):
        """
        Returns a list of all the distances between successive markers
        """
        distances = []
        for i in range(0, len(self.distance_markers) - 1):
            cur = self.distance_markers[i]
            _next = self.distance_markers[i+1]

            distances.append(_distance(cur.location, _next.location))

        return distances

    def __str__(self):
        return str([(m.location, m.distance, m.precision) for m in self.distance_markers])

    def to_circles(self):
        pass

def _distance(loc1, loc2):
    """
    Returns the Euclidean distance between two co-ordinates in
    km
    """
    R_EARTH = 6378.1

    lat1_rad = math.radians(loc1[0])
    lat2_rad = math.radians(loc2[0])
    lon1_rad = math.radians(loc1[1])
    lon2_rad = math.radians(loc2[1])
    delta_lat = lat1_rad - lat2_rad
    delta_lon = lon1_rad - lon2_rad

    a = (math.sin(delta_lat/2.0))**2 + (math.cos(lat1_rad)*math.cos(lat2_rad) * (math.sin(delta_lon/2.0))**2)
    c = 2 * math.atan2(a**0.5, (1-a)**0.5)
    d = R_EARTH * c

    return d

def _km_to_miles(miles):
    MILES_PER_KM = 0.621371
    return miles * MILES_PER_KM

def _distance_markers(attacker, target, n_distance_markers, direction, target_moves=False):
    """
    Given an attacker and a target, shuffle one of them in given direction until
    n_distance_marker distance markers have been accumulated
    """
    markers = []
    for i in range(0, n_distance_markers):
        m = _next_distance_marker(attacker, target, direction, target_moves)
        print((m.location, m.distance))

        markers.append(m)
    return DistanceMarkerSet(markers)

def _next_distance_marker(attacker, target, direction, target_moves=False):
    """
    Find the next distance marker between attacker and target
    """
    print("Looking for next_distance_marker")
    print("ATTACKER: %s" % str(attacker.location()))
    print("TARGET: %s" % str(target.location()))
    if target_moves:
        mover = target
        non_mover = attacker
    else:
        mover = attacker
        non_mover = target

    def with_precision(precision):
        print("precision: %.10f" % precision)
        last_dist = None
        pos = mover.location()

        while True:
            mover.move(pos)
            dist = mover.ping(non_mover.user_id())
            print pos
            print mover.location()
            print non_mover.location()
            print dist

            if dist != last_dist and last_dist is not None:
                av_dist = (dist + last_dist) / 2.0
                mover.move(last_pos)
                return DistanceMarker(last_pos, av_dist, precision)

            last_dist = dist
            last_pos = pos

            pos = (
                pos[0] + direction[0] * precision,
                pos[1] + direction[1] * precision
            )

    for dps in range(2, 4):
        prec = 10**-dps
        m = with_precision(prec)

    mover.move((
        m.location[0] + direction[0] * m.precision,
        m.location[1] + direction[1] * m.precision
    ))
    return m

LAT_RANGE = (37.5, 37.7)
LON_RANGE = (-122.5, -122.2)

def _random_location():
    return _round_location((random.uniform(*LAT_RANGE), random.uniform(*LON_RANGE)))

def _random_direction():
    x = random.uniform(-1, 1)

    y_sign = random.choice([-1, +1])
    y = y_sign * ((1 - x**2) ** 0.5)

    return (x, y)

def _round_location(loc, dps=DEFAULT_DPS):
    return (
        round(loc[0], dps),
        round(loc[1], dps)
    )

def _round(n, round_to):
    return round(n / round_to) * round_to

def _random_displacement(magnitude_range=(0.0, 0.1)):
    magnitude = random.uniform(*magnitude_range)
    direction = utils._random_direction()

    return (
        magnitude * direction[0],
        magnitude * direction[1]
    )

