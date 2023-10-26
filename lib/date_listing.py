
class DateListing:
    def __init__(self, id, date_available, listing_id, request_id):
        self.id = id
        self.date_available = date_available
        self.listing_id = listing_id
        self.request_id = request_id

    def __eq__(self, other):
        if not isinstance(other, DateListing):
            return False
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"DateListing({self.id}, {self.date_available}, {self.listing_id}, {self.request_id})"