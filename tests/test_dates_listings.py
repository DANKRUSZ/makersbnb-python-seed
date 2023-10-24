from datetime import date
from lib.dates_listings import DatesListings

def test_dateslistings_initiation():
    datelisting = DatesListings (1, date(2023, 10, 24), 2, 2)
    assert datelisting.id == 1
    assert datelisting.date_available == date(2023, 10, 24)
    assert datelisting.listing_id == 2
    assert datelisting.requester_id == 2

def test_eql():
    datelisting1 = DatesListings (1, date(2023, 10, 24), 2, 2)
    datelisting2 = DatesListings (1, date(2023, 10, 24), 2, 2)
    assert datelisting1 == datelisting2

def test_formats_nicely():
    datelisting = DatesListings (1, date(2023, 10, 24), 2, 2)
    assert str(datelisting) == "DatesListings(1, 2023-10-24, 2, 2)"


    