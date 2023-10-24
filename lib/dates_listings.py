
class DatesListings:
    def __init__(self, id, date_available, listing_id, requester_id):
        self.id = id
        self.date_available = date_available
        self.listing_id = listing_id
        self.requester_id = requester_id

    def __eq__(self, other):
        if not isinstance(other, DatesListings):
            return False
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"DatesListings({self.id}, {self.date_available}, {self.listing_id}, {self.requester_id})"