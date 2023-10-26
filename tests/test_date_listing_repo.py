from datetime import date
from lib.date_listing_repo import DateListingRepo
from lib.date_listing import DateListing
from datetime import datetime, timedelta

## DATES LISTINGS REPOSITORY ###########

# ==== ALL =========== #######
def test_all(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = DateListingRepo(db_connection)

    assert repository.all() == [
        DateListing(1, date(2023,10,24), 1, 1),
        DateListing(2, date(2023,10,24), 2, None),
        DateListing(3, date(2023,10,24), 3, None),
        DateListing(4, date(2023,10,24), 4, None)
    ]

# ====== FIND ========== #
def test_find(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = DateListingRepo(db_connection)

    assert repository.find(3) == DateListing(3, date(2023,10,24), 3, None)
    assert repository.find(5) == None

def test_find_by_listing_id(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = DateListingRepo(db_connection)

    assert repository.find_by_listing_id(2) == [DateListing(2, date(2023,10,24), 2, None)]
    assert repository.find_by_listing_id(4) == [DateListing(4, date(2023,10,24), 4, None)]

# ======= CREATE ======= #
def test_create(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = DateListingRepo(db_connection)

    assert repository.create(date(2023,10,23), 4, 3) == 5
    assert repository.all() == [
        DateListing(1, date(2023,10,24), 1, 1),
        DateListing(2, date(2023,10,24), 2, None),
        DateListing(3, date(2023,10,24), 3, None),
        DateListing(4, date(2023,10,24), 4, None),
        DateListing(5, date(2023,10,23), 4, 3)
        ]
    assert repository.create(date(2023,10,23), 4, None) == 6
    assert repository.all() == [
        DateListing(1, date(2023,10,24), 1, 1),
        DateListing(2, date(2023,10,24), 2, None),
        DateListing(3, date(2023,10,24), 3, None),
        DateListing(4, date(2023,10,24), 4, None),
        DateListing(5, date(2023,10,23), 4, 3),
        DateListing(6, date(2023,10,23), 4, None)
        ]


# ------- CREATE ERRORS HANDLING ---------
def test_check_for_errors_new_listing(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = DateListingRepo(db_connection)

    assert repository.check_for_errors_new_listing("", "") == True
    assert repository.check_for_errors_new_listing("2023-10-25", "2023-10-27") == True
    assert repository.check_for_errors_new_listing("2023-10-26", "2023-10-25") == True
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    next_week = today + timedelta(days=7)
    assert repository.check_for_errors_new_listing(today.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")) == False
    assert repository.check_for_errors_new_listing(tomorrow.strftime("%Y-%m-%d"), next_week.strftime("%Y-%m-%d")) == False

# ======= DELETE ======= #
def test_delete_DateListing(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = DateListingRepo(db_connection)

    repository.delete(1)
    assert repository.all() == [
        DateListing(2, date(2023,10,24), 2, None),
        DateListing(3, date(2023,10,24), 3, None),
        DateListing(4, date(2023,10,24), 4, None)
    ]