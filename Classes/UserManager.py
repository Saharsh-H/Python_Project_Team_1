class UserManager():
    def __init__(self, username, password):
        self._id = username
        self.password = password
        self.booked_flights = []
        self.booked_hotels = []
        self.booked_cars = []
