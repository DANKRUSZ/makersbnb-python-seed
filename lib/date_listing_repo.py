# CREATE, FIND DELETE
from lib.date_listing import DateListing

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
    def find_by_request_id(self, requester_id:int) -> DateListing:
        query = 'SELECT * FROM dates_listings WHERE request_id=%s'
        params = [requester_id]

        rows = self._connection.execute(query, params)
        return self.generate_datelistings(rows)
    

    # == CREATE NEW USER & ERRORS =============

    # Create a new datelisting, returning datelisting id
    # NOTE using create with fields instead of DateListing object for ease of error handling.
    
    def create(self, date_available, listing_id, requester_id=None):
        query = 'INSERT INTO dates_listings (date_available, listing_id, request_id) VALUES (%s, %s, %s) RETURNING id'
        params = [date_available, listing_id]
        rows = self._connection.execute(query, params)
        dates_listings_id = rows[0]['id']
        return dates_listings_id



    # == DELETE A USER =============

    # Delete a datelisting by id
    def delete(self, user_id) -> None:
        query = 'DELETE FROM dates_listings WHERE id = %s'
        params = [user_id]
        self._connection.execute(query, params)
        return None


    