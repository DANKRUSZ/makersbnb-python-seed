# CREATE, FIND DELETE
from lib.date_listing import DateListing

class DateListingRepo:
    def __init__(self, connection):
        self._connection = connection
    
    # generate multiple datelistings from SQL query rows
    def generate_datelistings(self, rows) -> list[DateListing]:
        datelistings = []
        for row in rows:
            datelisting = DateListing(row['id'], row['date_available'], row['listing_id'], row['requester_id'])
            datelistings.append(datelisting)
        return datelistings
    
    # generate a single datelisting from a SQL query row
    def generate_single_datelisting(self, rows) -> DateListing:
        if rows == []:
            return None
        row = rows[0]
        return DateListing(row['id'], row['date_available'], row['listing_id'], row['requester_id'])

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
    def find_by_requester_id(self, requester_id:int) -> DateListing:
        query = 'SELECT * FROM dates_listings WHERE requester_id=%s'
        params = [requester_id]

        rows = self._connection.execute(query, params)
        return self.generate_datelistings(rows)
    
    # # Find a single datelisting by email -- one unique email for each datelisting in the db
    # def find_by_email(self, email:str) -> DateListing or None:
    #     query = 'SELECT * FROM dates_listings WHERE email=%s'
    #     params = [email]

    #     rows = self._connection.execute(query, params)
    #     return self.generate_single_datelisting(rows)

    # == CREATE NEW USER & ERRORS =============

    # Create a new datelisting, returning datelisting id
    # NOTE using create with fields instead of DateListing object for ease of error handling.
    
    def create(self, date_available, listing_id, requester_id):
        query = 'INSERT INTO dates_listings (date_available, listing_id, requester_id) VALUES (%s, %s, %s) RETURNING id'
        params = [date_available, listing_id, requester_id]
        rows = self._connection.execute(query, params)
        dates_listings_id = rows[0]['id']
        return dates_listings_id

    # Check for duplicate email
    def check_for_duplicate_registration(self, email:str) -> list:
        errors = []
        same_email_rows = self._connection.execute('SELECT id FROM dates_listings WHERE email = %s', [email])
        if same_email_rows != []:
            errors.append("Email is already registered with an account")
        return errors

    # Check if fields for creating a new datelisting are valid
    def is_valid(self, email:str, password:str) -> list:
        errors = []
        if email == None or email == "":
            errors.append("Email cannot be empty")
        elif "@" not in email: #TODO Refine this!
            errors.append("Invalid email address")

        if password == None or password == "":
            errors.append("Password cannot be empty")
        elif len(password) <= 8:
            errors.append("Password must be 8 chars or longer")
        # TODO: Add additional rules for password such as needing one num, one special char, one lowercase letter, one upper case letter
        return errors

    # Generate errors as a string #TODO add additional errors lists here such as password lenght, etc
    def generate_errors(self, is_valid_errors) -> None or str:
        if is_valid_errors == []:
            return None
        return ", ".join(is_valid_errors)


    # == DELETE A USER =============

    # Delete a datelisting by id
    def delete(self, user_id) -> None:
        query = 'DELETE FROM dates_listings WHERE id = %s'
        params = [user_id]
        self._connection.execute(query, params)
        return None


    