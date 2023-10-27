from lib.request import Request
class RequestRepository:
    def __init__(self, connection):
        self._connection = connection

    # generate multiple requests from SQL query rows
    def generate_requests(self, rows) -> list[Request]:
        requests = []
        for row in rows:
            request = Request(row['id'], row['date_requested'], row['listing_id'], row['requester_id'], row['confirmed'])
            requests.append(request)
        return requests
    
    # generate a single request from a SQL query row
    def generate_single_request(self, rows) -> Request:
        if rows == []:
            return None
        row = rows[0]
        return Request(row['id'], row['date_requested'], row['listing_id'], row['requester_id'], row['confirmed'])

    # == ALL REQUESTS ===
    # Retrieve all registered requests from db
    def all(self) -> list[Request]:
        query = 'SELECT * FROM requests'
        rows = self._connection.execute(query)
        return self.generate_requests(rows)
    

    # == FIND REQUEST/REQUESTS =============

    # Find a single request by id
    def find(self, request_id:int) -> Request:
        query = 'SELECT * FROM requests WHERE id=%s'
        params = [request_id]

        rows = self._connection.execute(query, params)
        return self.generate_single_request(rows)
    

        # Find request/requests with same requester id
    def find_by_requester_id(self, requester_id:int) -> Request:
        query = 'SELECT * FROM requests WHERE requester_id=%s'
        params = [requester_id]

        rows = self._connection.execute(query, params)
        return self.generate_requests(rows)
    
    # ==== CREATE REQUEST ====

    def create(self, date_requested, listing_id, requester_id, confirmed):
        query = 'INSERT INTO requests (date_requested, listing_id, requester_id, confirmed) VALUES (%s, %s, %s, %s) RETURNING id'
        params = [date_requested, listing_id, requester_id, confirmed]
        rows = self._connection.execute(query, params)
        request_id = rows[0]['id']
        return request_id
    
    # == DELETE A REQUEST =============

    # Delete a request by id
    def delete(self, request_id) -> None:
        query = 'DELETE FROM requests WHERE id = %s'
        params = [request_id]
        self._connection.execute(query, params)
        return None
    
    
    # ===== CONFIRM A REQUEST =====

    def confirm(self, request_id):
        query = 'UPDATE requests SET confirmed = True WHERE id = %s'
        params = [request_id]

        self._connection.execute(query, params)
        return None
    
    # ===== DENY A REQUEST =====

    def deny(self, request_id):
        query = 'UPDATE requests SET confirmed = False WHERE id = %s'
        params = [request_id]

        self._connection.execute(query, params)
        return None
    

    # ===== CHECK REQUESTS RECEIVED =====
    #TODO please update test for this
    def requests_received(self, owner_id):
        query = 'SELECT requests.id, requests.date_requested, requests.listing_id, requests.requester_id,requests.confirmed, listings.title FROM requests JOIN listings ON requests.listing_id = listings.id WHERE listings.owner_id = %s'
        params = [owner_id]

        rows = self._connection.execute(query, params)
        result = []
        for row in rows:
            if row['confirmed'] == None:
                confirmation = "Not confirmed"
            elif row['confirmed'] == True:
                confirmation = "Confirmed"
            elif row['confirmed'] == False:
                confirmation == "Denied"

            request = {'id': row['id'],
                    'date_requested': row['date_requested'],
                    'listing_id': row['listing_id'],
                    'requester_id': row['requester_id'],
                    'confirmed': confirmation,
                    'title': row['title']
                    }
            result.append(request)
        return result

    # ===== CHECK REQUESTS I HAVE MADE =====
    #TODO please update test for this
    def requests_made(self, requester_id):
        query = 'SELECT requests.id, requests.date_requested, requests.listing_id, requests.requester_id,requests.confirmed, listings.title FROM requests JOIN listings ON requests.listing_id = listings.id WHERE requests.requester_id = %s'
        params = [requester_id]

        rows = self._connection.execute(query, params)
        result = []
        for row in rows:
            if row['confirmed'] == None:
                confirmation = "Not confirmed"
            elif row['confirmed'] == True:
                confirmation = "Confirmed"
            elif row['confirmed'] == False:
                confirmation == "Denied"

            request = {'id': row['id'],
                    'date_requested': row['date_requested'],
                    'listing_id': row['listing_id'],
                    'requester_id': row['requester_id'],
                    'confirmed': confirmation,
                    'title': row['title']
                    }
            result.append(request)
        return result

    # ===== CHECK IF I OWN THE REQUESTED LISTING =========
    #TODO Please write test for this
    def check_if_owned_by(self, request_id, user_id):
        query = 'SELECT requests.id, requests.date_requested, requests.listing_id, requests.requester_id,requests.confirmed, listings.title FROM requests JOIN listings ON requests.listing_id = listings.id WHERE listings.owner_id = %s AND requests.id = %s'
        params = [user_id, request_id]
        rows = self._connection.execute(query, params)
        if rows != []:
            return True
        return False


    # ====== FIND THIS REQUEST & LISTING DETAILS ==========
    #TODO Please write test for this
    def find_this_request_details(self, request_id):
        query = 'SELECT requests.id, requests.date_requested, requests.listing_id, requests.requester_id,requests.confirmed, listings.title, listings.description FROM requests JOIN listings ON requests.listing_id = listings.id WHERE requests.id = %s'
        params = [id]

        rows = self._connection.execute(query, params)
        result = []
        for row in rows:
            if row['confirmed'] == None:
                confirmation = "Not confirmed"
            elif row['confirmed'] == True:
                confirmation = "Confirmed"
            elif row['confirmed'] == False:
                confirmation == "Denied"

            request = {'id': row['id'],
                    'date_requested': row['date_requested'],
                    'listing_id': row['listing_id'],
                    'requester_id': row['requester_id'],
                    'confirmed': confirmation,
                    'title': row['title'],
                    'description': row['description']
                    }
            result.append(request)
        return result[0]

    def find_owner_email(self, listing_id):
        query = 'SELECT users.id, users.email FROM users JOIN listing ON listings.owner_id = users.id WHERE lists.id = %s'
        params = [listing_id]
        rows = self._connection.execute(query, params)
        return rows[0]['email']


    # # ====== FIND OTHER REQUESTS FOR THIS LISTING ==========
    # #TODO Please write test for this
    # def find_other_requests(self, request:Request):
    #     listing_id = request.listing_id
    #     this_request_id = request.id

    #     query = 'SELECT requests.id, requests.date_requested, requests.listing_id, requests.requester_id,requests.confirmed, listings.title FROM requests JOIN listings ON requests.listing_id = listings.id WHERE listings.id = %s AND requests.id != %s'
    #     params = [listing_id, this_request_id]

    #     rows = self._connection.execute(query, params)
    #     result = []
    #     for row in rows:
    #         if row['confirmed'] == None:
    #             confirmation = "Not confirmed"
    #         elif row['confirmed'] == True:
    #             confirmation = "Confirmed"
    #         elif row['confirmed'] == False:
    #             confirmation == "Denied"

    #         request = {'id': row['id'],
    #                 'date_requested': row['date_requested'],
    #                 'listing_id': row['listing_id'],
    #                 'requester_id': row['requester_id'],
    #                 'confirmed': confirmation,
    #                 'title': row['title']
    #                 }
    #         result.append(request)
    #     return result
