from TravelManager import TravelManager


class FlightManager(TravelManager):
    def __init__(self, _id, price, duration,source, destination, airline, departure_time, seats_available):
        super().__init__(_id, price, duration, destination)
        self.airline = airline
        self.source = source
        self.departure_time = departure_time
        self.seats_available = seats_available

    def get_details(self):
        details = super().get_details()
        details.update({
            "airline": self.airline,
            "source": self.source,
            "departure_time": self.departure_time,
            "seats_available": self.seats_available
        })
        return details