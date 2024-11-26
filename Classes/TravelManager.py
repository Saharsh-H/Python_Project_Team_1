
class TravelManager:
    def __init__(self, _id, price, duration, destination):
        self._id = _id
        self.availability = True
        self.price = price
        self.duration = duration
        self.destination = destination

    def get_details(self):
        return {
            "id": self._id,
            "availability": self.availability,
            "price": self.price,
            "duration": self.duration,
            "destination": self.destination
        }