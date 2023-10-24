from lib.listing import *
    
        
class ListingRepository():
    def __init__(self, connection):
        self._connection = connection

    def generate_listings(self, rows):
        listings = []
        for row in rows:
            listing = Listing(row['id'], row['title'], row['description'], row['price'], row['owner_id'])
            listings.append(listing)
        return listings
    
    def generate_single_listing(self, rows):
        pass
        
    def create(self):
        pass

    def find(self):
        pass

    def delete(self):
        pass

    def all(self): # Like find but showing everything in the table
        query = 'SELECT * FROM listings'
        rows = self._connection.execute(query)
        return self.generate_listings(rows)
