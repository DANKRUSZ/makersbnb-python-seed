

class Request:
    def __init__(self, id, date_requested, listing_id, requester_id, confirmed):
        self.id = id
        self.date_requested = date_requested
        self.listing_id = listing_id
        self.requester_id = requester_id
        self.confirmed = confirmed

    def __eq__(self, other):
        if not isinstance(other, Request):
            return False
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Request({self.id}, {self.date_requested}, {self.listing_id}, {self.requester_id}, {self.confirmed})"