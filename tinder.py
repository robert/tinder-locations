import time
from interfaces import *

class TinderUser(User):

    MIN_CO_ORD_DELTA = 0.02

    def __init__(self, session):
        self.session = session
        self._user_id = None

    def user_id(self):
        if self._user_id is None:
            self._user_id = self._fetch_user_id()

        return self._user_id

    def move(self, co_ords):
        res = self._with_retries(
            lambda: self.session.update_location(co_ords[0]+self.MIN_CO_ORD_DELTA, co_ords[1]+self.MIN_CO_ORD_DELTA))
        assert(200 == res['status'])

        res2 = self._with_retries(
            lambda: self.session.update_location(co_ords[0], co_ords[1]))
        assert(200 == res['status'])

    def ping(self, pingee_id):
        response = self.session._api.user_info(str(pingee_id))
        distance = response['results']["distance_mi"]
        if distance is None:
            pprint(self.location())
        return distance

    def location(self):
        profile = self.profile()
        return (profile['pos']['lat'], profile['pos']['lon'])

    def profile(self):
        return self.session._api.profile()

    def _fetch_user_id(self):
        return self.profile()['_id']

    def _with_retries(self, f):
        ret = None
        max_retries = 5
        for i in range(0, max_retries):
            try:
                ret = f()
                break
            except Exception as ex:
                print("Exception: %s" % ex)
                time.sleep(1)
                if i == max_retries:
                    raise

        return ret

