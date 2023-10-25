from lib.listing_repository import *
from lib.listing import *

'''
When we call the all method
It returns all rows in the listing table as a list of objects
'''

def test_all(db_connection):
    db_connection.seed('seeds/makers_bnb.sql')
    repository = ListingRepository(db_connection)
    assert repository.all() == [
        Listing(1, 'House 1', 'Small house', 100.00, 1),
        Listing(2, 'House 2', 'Medium house', 150.00, 2),
        Listing(3, 'House 3', 'Big house', 200.00, 3),
        Listing(4, 'House 4', 'Massive house', 500.00, 4)]
        

'''
Testing create method
'''

def test_create(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = ListingRepository(db_connection)

    assert repository.create('House 5', 'Description5', 75.00, 2)
    assert repository.all() == [
        Listing(1, 'House 1', 'Small house', 100.00, 1),
        Listing(2, 'House 2', 'Medium house', 150.00, 2),
        Listing(3, 'House 3', 'Big house', 200.00, 3),
        Listing(4, 'House 4', 'Massive house', 500.00, 4),
        Listing(5, 'House 5', 'Description5', 75.00, 2)
        ]


'''
Testing find method, 
'''
def test_find(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = ListingRepository(db_connection)

    assert repository.find(3) == Listing(3, 'House 3', 'Big house', 200.00, 3)
    assert repository.find(5) == None


'''
Test find method returning multiple objects
To be adapted
'''
# def test_find_by_requester_id(db_connection):
#     db_connection.seed("seeds/makers_bnb.sql")
#     repository = DateListingRepo(db_connection)

#     assert repository.find_by_requester_id(1) == [DateListing(2, date(2023,10,24), 2, 1), DateListing(4, date(2023,10,24), 4, 1)]
#     assert repository.find_by_requester_id(5) == []


# ======= DELETE listing======= #
def test_delete_Listing(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = ListingRepository(db_connection)

    repository.delete(1)
    assert repository.all() == [
        Listing(2, 'House 2', 'Medium house', 150.00, 2),
        Listing(3, 'House 3', 'Big house', 200.00, 3),
        Listing(4, 'House 4', 'Massive house', 500.00, 4)
    ]