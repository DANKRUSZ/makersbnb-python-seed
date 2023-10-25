from datetime import date
from lib.date_listing import DateListing

def test_DateListing_initiation():
    datelisting = DateListing (1, date(2023, 10, 24), 2, 2)
    assert datelisting.id == 1
    assert datelisting.date_available == date(2023, 10, 24)
    assert datelisting.listing_id == 2
    assert datelisting.requester_id == 2

def test_eql():
    datelisting1 = DateListing (1, date(2023, 10, 24), 2, 2)
    datelisting2 = DateListing (1, date(2023, 10, 24), 2, 2)
    assert datelisting1 == datelisting2

def test_formats_nicely():
    datelisting = DateListing (1, date(2023, 10, 24), 2, 2)
    assert str(datelisting) == "DateListing(1, 2023-10-24, 2, 2)"


    