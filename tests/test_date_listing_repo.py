from datetime import date
from lib.date_listing_repo import DateListingRepo
from lib.date_listing import DateListing

## DATES LISTINGS REPOSITORY ###########

# ==== ALL =========== #######
def test_all(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = DateListingRepo(db_connection)

    assert repository.all() == [
        DateListing(1, date(2023,10,24), 1, 3),
        DateListing(2, date(2023,10,24), 2, 1),
        DateListing(3, date(2023,10,24), 3, 2),
        DateListing(4, date(2023,10,24), 4, 1)
    ]

# ====== FIND ========== #
def test_find(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = DateListingRepo(db_connection)

    assert repository.find(3) == DateListing(3, date(2023,10,24), 3, 2)
    assert repository.find(5) == None

def test_find_by_requester_id(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = DateListingRepo(db_connection)

    assert repository.find_by_requester_id(1) == [DateListing(2, date(2023,10,24), 2, 1), DateListing(4, date(2023,10,24), 4, 1)]
    assert repository.find_by_requester_id(5) == []

# ======= CREATE ======= #
def test_create(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = DateListingRepo(db_connection)

    assert repository.create(date(2023,10,23), 4, 3) == 5
    assert repository.all() == [
        DateListing(1, date(2023,10,24), 1, 3),
        DateListing(2, date(2023,10,24), 2, 1),
        DateListing(3, date(2023,10,24), 3, 2),
        DateListing(4, date(2023,10,24), 4, 1),
        DateListing(5, date(2023,10,23), 4, 3)
        ]

# ======= DELETE ======= #
def test_delete_DateListing(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = DateListingRepo(db_connection)

    repository.delete(1)
    assert repository.all() == [
        DateListing(2, date(2023,10,24), 2, 1),
        DateListing(3, date(2023,10,24), 3, 2),
        DateListing(4, date(2023,10,24), 4, 1)
    ]