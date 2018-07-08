from interfaces import *
import utils

class FakeService:

    def __init__(self):
        self.locations = {}

    def move(self, user_id, location):
        self.locations[user_id] = location

    def ping(self, pinger_id, pingee_id):
        pinger_loc = self.location(pinger_id)
        pingee_loc = self.location(pingee_id)

        distance = utils._distance(pinger_loc, pingee_loc)

        return round(distance)

    def location(self, user_id):
        loc = self.locations[user_id]
        return utils._round_location(loc)

class FakeUser(User):

    def __init__(self, user_id, initial_location, service):
        self._user_id = user_id
        self.service = service

        self.move(initial_location)

    def user_id(self):
        return self._user_id

    def move(self, co_ords):
        self.service.move(self.user_id(), co_ords)

    def ping(self, pingee_id):
        return self.service.ping(self.user_id(), pingee_id)

    def location(self):
        return self.service.location(self.user_id())


