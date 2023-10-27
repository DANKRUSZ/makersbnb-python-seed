from lib.listing import *
from datetime import datetime, timedelta
        
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

    # ======= FIND AVAILABLE LISTINGS BETWEEN A DATE RANGE ==============

    def find_available_listings_for_dates(self, available_from, available_to):
        # make a list of date objects in the range available_from to available_to, inclusive
        dates_list = []
        working_date = available_from
        while working_date <= available_to:
            dates_list.append(working_date)
            working_date += timedelta(days=1)
        dates_strings_list = [date.strftime('%Y-%m-%d') for date in dates_list]

        # make sql query for listings JOIN dates_listings on listing_id WHERE date_available is in the date range
        query = 'SELECT listings.id, listings.title, listings.description, listings.price, listings.owner_id FROM listings JOIN dates_listings ON listings.id = dates_listings.listing_id WHERE dates_listings.date_available = ANY(%s)'
        params = (dates_strings_list,) 

        rows = self._connection.execute(query, params)
        # generate listing objects from those rows
        return self.generate_listings(rows)


    # ------------------ ERRORS FROM SEARCH ----------------------------

    def check_search_for_errors(self, available_from, available_to):
        # Check if either available_from or available_to is None or empty
        if available_from in [None, ""] or available_to in [None, ""]:
            return True
        
        try:
            # Parse date strings into datetime objects
            date_available_from = datetime.strptime(available_from, '%Y-%m-%d')
            date_available_to = datetime.strptime(available_to, '%Y-%m-%d')
            
            # # Get today's date
            # date_today = datetime.now()
            # date_today = date_today.replace(hour=0, minute=0, second=0, microsecond=0)
            
            # # Check if available_from is on or after today's date
            # if date_available_from < date_today:
            #     return True
            
            # Check if available_to is on or after available_from
            if date_available_to < date_available_from:
                return True
            
        except ValueError:
            # Handle invalid date format
            return True

        # If none of the error conditions are met, return False
        return False

    def generate_search_errors(self, available_from, available_to):
        errors = []
        # Check if either available_from or available_to is None or empty
        if available_from in [None, ""] or available_to in [None, ""]:
            if available_from in [None, ""]:
                errors.append("Date Available From cannot be blank")
            if available_to in [None, ""]:
                errors.append("Date Available To cannot be blank")
        
        try:
            # Parse date strings into datetime objects
            date_available_from = datetime.strptime(available_from, '%Y-%m-%d')
            date_available_to = datetime.strptime(available_to, '%Y-%m-%d')
            
            # # Get today's date
            # date_today = datetime.now()
            # date_today = date_today.replace(hour=0, minute=0, second=0, microsecond=0)
            
            # # Check if available_from is on or after today's date
            # if date_available_from < date_today:
            #     errors.append("Date Available From must be on or after today's date")
            
            # Check if available_to is on or after available_from
            if date_available_to < date_available_from:
                errors.append("Date Available To must be on or after Date Available From")
            
        except ValueError:
            # Handle invalid date format
            pass
            # errors.append("Invalid date format")

        return ", ".join(errors)
    





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

