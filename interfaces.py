from utils import *
from pprint import pprint
import random

class User:

    def move(self, co_ords):
        pass

    def ping(self, pingee_id):
        pass

class Attack:

    def run(self):
        pass

class AttackOutput:

    def save_kml(self):
        pass

    def location_estimate(self):
        pass

class Property:

    def name(self):
        pass

    def description(self):
        pass

    def multi_evaluate(self, user1, user2, n_evals, seed=None):
        if seed is None:
            seed = random.randint(0, 9999)
        random.seed(seed)
        print("Seed = %d" % seed)
        print("Running %s" % self.__class__.__name__)
        results = []
        for _ in range(0, n_evals):
            inputs = self.generate_inputs()
            pprint(inputs)
            ret = self.evaluate(user1, user2, inputs)
            # pprint(ret)
            results.append(ret)
        return results

    def generate_inputs(self):
        pass

    def evaluate(self, user1, user2, inputs):
        pass

