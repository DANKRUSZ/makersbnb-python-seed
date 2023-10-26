# CREATE, FIND DELETE
from lib.date_listing import DateListing
from datetime import datetime

class DateListingRepo:
    def __init__(self, connection):
        self._connection = connection
    
    # generate multiple datelistings from SQL query rows
    def generate_datelistings(self, rows) -> list[DateListing]:
        datelistings = []
        for row in rows:
            datelisting = DateListing(row['id'], row['date_available'], row['listing_id'], row['request_id'])
            datelistings.append(datelisting)
        return datelistings
    
    # generate a single datelisting from a SQL query row
    def generate_single_datelisting(self, rows) -> DateListing:
        if rows == []:
            return None
        row = rows[0]
        return DateListing(row['id'], row['date_available'], row['listing_id'], row['request_id'])

    # == ALL DATE LISTINGS ===
    # Retrieve all registered datelistings from db
    def all(self) -> list[DateListing]:
        query = 'SELECT * FROM dates_listings'
        rows = self._connection.execute(query)
        return self.generate_datelistings(rows)

    # == FIND SINGLE DATE LISTINGS =============

    # Find a single datelisting by id
    def find(self, dateslistings_id:int) -> DateListing:
        query = 'SELECT * FROM dates_listings WHERE id=%s'
        params = [dateslistings_id]

        rows = self._connection.execute(query, params)
        return self.generate_single_datelisting(rows)
    

        # Find datelisting by requester id
    def find_by_listing_id(self, listing_id:int) -> DateListing:
        query = 'SELECT * FROM dates_listings WHERE listing_id=%s'
        params = [listing_id]

        rows = self._connection.execute(query, params)
        return self.generate_datelistings(rows)
    

    # == CREATE NEW USER & ERRORS =============

    # Create a new datelisting, returning datelisting id
    
    def create(self, date_available, listing_id, request_id=None):
        query = 'INSERT INTO dates_listings (date_available, listing_id, request_id) VALUES (%s, %s, %s) RETURNING id'
        params = [date_available, listing_id, request_id]
        rows = self._connection.execute(query, params)
        dates_listings_id = rows[0]['id']
        return dates_listings_id

    # ----- CREATE FIELDS ERROR HANDLING ---------- #

    def check_for_errors_new_listing(self, available_from:str, available_to:str) -> bool:
        # Check if either available_from or available_to is None or empty
        if available_from in [None, ""] or available_to in [None, ""]:
            return True
        
        try:
            # Parse date strings into datetime objects
            date_available_from = datetime.strptime(available_from, '%Y-%m-%d')
            date_available_to = datetime.strptime(available_to, '%Y-%m-%d')
            
            # Get today's date
            date_today = datetime.now()
            date_today = date_today.replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Check if available_from is on or after today's date
            if date_available_from < date_today:
                return True
            
            # Check if available_to is on or after available_from
            if date_available_to < date_available_from:
                return True
            
        except ValueError:
            # Handle invalid date format
            return True

        # If none of the error conditions are met, return False
        return False


    def generate_errors_new_listing(self, available_from:str, available_to:str):
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
            
            # Get today's date
            date_today = datetime.now()
            date_today = date_today.replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Check if available_from is on or after today's date
            if date_available_from < date_today:
                errors.append("Date Available From must be on or after today's date")
            
            # Check if available_to is on or after available_from
            if date_available_to < date_available_from:
                errors.append("Date Available To must be on or after Date Available From")
            
        except ValueError:
            # Handle invalid date format
            pass
            # errors.append("Invalid date format")

        return ", ".join(errors)

    # == DELETE A USER =============

    # Delete a datelisting by id
    def delete(self, user_id) -> None:
        query = 'DELETE FROM dates_listings WHERE id = %s'
        params = [user_id]
        self._connection.execute(query, params)
        return None


    