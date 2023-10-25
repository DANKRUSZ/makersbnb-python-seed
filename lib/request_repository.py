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