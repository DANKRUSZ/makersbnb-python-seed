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
    
    # ==== ALL LISTINGS ==============

    def all(self): 
        query = 'SELECT * FROM listings'
        rows = self._connection.execute(query)
        return self.generate_listings(rows)

    # ==== FIND LISTINGS ==============

    def find(self, listing_id:int) -> Listing:
        query = 'SELECT * FROM listings WHERE id=%s'
        params = [listing_id]

        rows = self._connection.execute(query, params)
        return self.generate_single_listing(rows)
    
    def find_by_owner_id(self, owner_id:int) -> Listing:
        query = 'SELECT * FROM listings WHERE owner_id=%s'
        params = [owner_id]
        rows = self._connection.execute(query, params)
        return self.generate_listings(rows)

    # ==== CREATE LISTING ==============
    
    def create(self, title:str, description:str, price:int, owner_id:int):
        query = 'INSERT INTO listings (title, description, price, owner_id) VALUES (%s, %s, %s, %s) RETURNING id'
        params = [title, description, price, owner_id]
        rows = self._connection.execute(query, params)
        listing_id = rows[0]['id']
        return listing_id

    # ------ CREATE LISTING ERRORS ----------

    def check_for_errors(self, title:str, description:str, price_string:str):
        error_exists = False
        # Check for blank fields
        if title in ["", None] or description in ["", None] or price_string in ["", None]:
            error_exists = True
        # Check price_string is numeric (ie. an integer)
        if not price_string.isnumeric() and price_string not in ["", None]:
            error_exists = True
        return error_exists
    
    def generate_errors(self, title:str, description:str, price_string:str):
        errors = []
        # Check for blank fields
        if title in ["", None]:
            errors.append("Name cannot be empty")
        if description in ["", None]:
            errors.append("Description cannot be empty")
        if price_string in ["", None]:
            errors.append("Price cannot be empty")
        # Check price_string is numeric
        if not price_string.isnumeric() and price_string not in ["", None]:
            errors.append("Price must be a whole number")
        return ", ".join(errors)

#TODO - related to the filtering of spaces on the all spaces page - SQL not working!!
    def get_available_spaces(self, date_from, date_to):
        query = "SELECT * FROM listings LEFT JOIN requests ON listings.id = listing_id WHERE (requester_id IS NULL OR (date_requested NOT BETWEEN %s AND %s));"
        rows = self._connection.execute(query, (date_to, date_from))
        print(rows)
        available_listings = []
        for row in rows:
            available_listings.append(row.id)
        return available_listings

  # == DELETE A LISTING =============

    # Delete a listing by id
    def delete(self, listing_id:int) -> Listing:
        query = 'DELETE FROM listings WHERE id = %s'
        params = [listing_id]
        self._connection.execute(query, params)
        return None

