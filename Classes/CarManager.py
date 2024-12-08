from Classes.TravelManager import TravelManager
class CarManager(TravelManager):
    def __init__(self, _id, price, duration,source, destination, car_model, rental_company):
        super().__init__(_id, price, duration, destination)
        self.car_model = car_model
        self.source = source
        self.rental_company = rental_company

    def get_details(self):
        details = super().get_details()
        details.update({
            "car_model": self.car_model,
            "source": self.source,
            "rental_company": self.rental_company
        })
        return details