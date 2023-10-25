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