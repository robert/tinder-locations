import time
import setup
import config
import kml
import random
import math
from pprint import pprint

from tinder import TinderUser
from happn import HappnClient, HappnUser
from fake import *
from utils import *
from interfaces import *

import utils


class DistanceMarkerPatternsParallel(Property):

    INITIAL_LOCATION_DELTA = 0.010

    def generate_inputs(self):
        return {
            'location': (37.749, -122.372),
            'distance_marker_direction': (1, 0),
            'initial_location_direction': (1, 0)
        }

    def evaluate(self, attacker, target, inputs):
        loc = inputs['location']
        distance_marker_direction = inputs['distance_marker_direction']
        initial_location_direction = inputs['initial_location_direction']

        n_markers = 6

        attacker.move(loc)
        target.move(loc)
        print attacker.location()
        print target.location()
        print attacker.ping(target.user_id())

        points = []
        points.append(("TARGET", target.location()))

        def run_f(direction, i):
            return utils._distance_markers(attacker, target, n_markers, direction)

        def process_f(distance_marker_set, i):
            for m in distance_marker_set.distance_markers:
                key = "%.1f" % m.distance
                points.append((key, m.location))
                print utils._distance(target.location(), m.location)
            kml.points(points, "%s-%d" % (time.time(), i))

        stream = _axis_pair_test_case_stream(loc, self.INITIAL_LOCATION_DELTA, 6)

        pprint([(tc.attacker_loc, tc.target_loc, tc.direction) for tc in stream])

        _run_over_stream(attacker, target, run_f, process_f, stream)

        kml.points(points)

class TestCase:

    def __init__(self, attacker_loc, target_loc, direction):
        """
        Attacker starts at attacker_loc
        Target starts at target_loc
        Attacker shuffles in direction 
        """
        self.attacker_loc = attacker_loc
        self.target_loc = target_loc
        self.direction = direction

def _linear_test_case_stream(centre, line_direction, delta, amp, test_case_direction, target_loc=None):
    """
    Return a line of test cases.
    """
    def mk(loc):
        if target_loc:
            tl = target_loc
        else:
            tl = loc
        return TestCase(loc, tl, test_case_direction)

    return map(mk, _linear_location_stream(centre, line_direction, delta, amp))

def _linear_location_stream(centre, line_direction, delta, amp):
    """
    Return a line of locations either side of given centre.
    """
    return [(
        centre[0] + line_direction[0] * n * delta,
        centre[1] + line_direction[1] * n * delta
    ) for n in range(-amp, amp+1)]

def _square_test_case_stream(centre, delta, amp):
    """
    Return a single square of test cases.
    """
    dirs = [(-1,0), (1,0), (0,-1), (0,1)]
    stream = []
    for d in dirs:
        line_dir = (1-abs(d[0]), 1-abs(d[1]))
        stream += _linear_test_case_stream(centre, line_dir, delta, amp, d, centre) 
    return stream

def _axis_pair_test_case_stream(centre, delta, amp):
    """
    Return an axis of test cases that rake across the given centre
    """
    c1 = (centre[0] - delta*amp, centre[1])
    c2 = (centre[0], centre[1] - delta*amp)

    line_dir1 = (0, 1)
    test_case_dir1 = (1, 0)
    line_dir2 = (1, 0)
    test_case_dir2 = (0, 1)

    return _linear_test_case_stream(c1, line_dir1, delta, amp, test_case_dir1, centre) + _linear_test_case_stream(c2, line_dir2, delta, amp, test_case_dir2, centre)



def _run_over_stream(attacker, target, run_f, process_f, test_case_stream):
    rets = []
    for i, tc in enumerate(test_case_stream):
        attacker.move(tc.attacker_loc)
        target.move(tc.target_loc)
        ret = run_f(tc.direction, i)
        processed = process_f(ret, i)
        rets.append(processed)

    return rets


live = True
attacker = None
target = None
seed = 1234

if live:
    attacker_session = setup.setup(
        config.ATTACKER_FB_EMAIL,
        config.ATTACKER_FB_PASSWORD,
    )
    target_session = setup.setup(
        config.TARGET_FB_EMAIL,
        config.TARGET_FB_PASSWORD,
    )
    attacker = TinderUser(attacker_session)
    target = TinderUser(target_session)
else:
    service = FakeService()
    attacker = FakeUser(1, (0,0), service)
    target = FakeUser(2, (3,5), service)

print "Attacker ID: %s" % attacker.user_id()
print "Target ID: %s" % target.user_id()

print(attacker.location())
prop = DistanceMarkerPatternsParallel()
o = prop.multi_evaluate(attacker, target, 1, seed)
exit(0)
