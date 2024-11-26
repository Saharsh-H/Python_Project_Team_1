from TravelManager import TravelManager


class HotelManager(TravelManager):
    def __init__(self, _id, price, duration, destination, hotel_name, rating, rooms_available):
        super().__init__(_id, price, duration, destination)
        self.hotel_name = hotel_name
        self.rating = rating
        self.rooms_available = rooms_available

    def get_details(self):
        details = super().get_details()
        details.update({
            "hotel_name": self.hotel_name,
            "rating": self.rating,
            "rooms_available": self.rooms_available
        })
        return details
