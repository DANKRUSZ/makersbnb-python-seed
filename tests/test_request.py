from datetime import date
from lib.request import Request

def test_request_initiation():
    request = Request (1, date(2023, 10, 24), 2, 2, None)
    assert request.id == 1
    assert request.date_requested == date(2023, 10, 24)
    assert request.listing_id == 2
    assert request.requester_id == 2
    assert request.confirmed == None

def test_eql():
    request1 = Request(1, date(2023, 10, 24), 2, 2, True)
    request2 = Request(1, date(2023, 10, 24), 2, 2, True)
    assert request1 == request2

def test_formats_nicely():
    request = Request(1, date(2023, 10, 24), 2, 2, None)
    assert str(request) == "Request(1, 2023-10-24, 2, 2, None)"