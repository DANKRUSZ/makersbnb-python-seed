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
        
