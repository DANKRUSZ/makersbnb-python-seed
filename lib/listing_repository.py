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
    
    # generate a single listing from a SQL query row
    def generate_single_listing(self, rows) -> Listing:
        if rows == []:
            return None
        row = rows[0]
        return Listing(row['id'], row['title'], row['description'], row['price'], row['owner_id'])
    
        
    def create(self, title, description, price, owner_id):
        query = 'INSERT INTO listings (title, description, price, owner_id) VALUES (%s, %s, %s, %s) RETURNING id'
        params = [title, description, price, owner_id]
        rows = self._connection.execute(query, params)
        listing_id = rows[0]['id']
        return listing_id

    def find(self, listing_id:int) -> Listing:
        query = 'SELECT * FROM listings WHERE id=%s'
        params = [listing_id]

        rows = self._connection.execute(query, params)
        return self.generate_single_listing(rows)

  # == DELETE A LISTING =============

    # Delete a listing by id
    def delete(self, listing_id:int) -> Listing:
        query = 'DELETE FROM listings WHERE id = %s'
        params = [listing_id]
        self._connection.execute(query, params)
        return None

    def all(self): # Like find but showing everything in the table
        query = 'SELECT * FROM listings'
        rows = self._connection.execute(query)
        return self.generate_listings(rows)
