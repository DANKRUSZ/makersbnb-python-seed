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
    repository.create('House 5', 'Description5', 75.00, 2)
    assert repository.find(3) == Listing(3, 'House 3', 'Big house', 200.00, 3)
    assert repository.find(6) == None
'''
Test find method returning multiple objects
To be adapted
'''
def test_find_by_owner_id(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = ListingRepository(db_connection)
    repository.create('House 5', 'Description5', 75.00, 2)
    assert repository.find_by_owner_id(2) == [
        Listing(2, 'House 2', 'Medium house', 150.00, 2), Listing(5, 'House 5', 'Description5', 75.00, 2)]
    assert repository.find_by_owner_id(5) == []

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

# ======== ERROR HANDLING FOR FORM FIELDS ======== #
def test_check_for_errors(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = ListingRepository(db_connection)

    assert repository.check_for_errors(title="", description="", price_string="") == True
    assert repository.check_for_errors(title="", description="some description", price_string="abc") == True
    assert repository.check_for_errors(title="", description="some description", price_string="1.5") == True
    assert repository.check_for_errors(title="Valid", description="Valid description", price_string="100") == False

def test_generate_errors(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = ListingRepository(db_connection)

    assert repository.generate_errors(title="", description="", price_string="") == "Name cannot be empty, Description cannot be empty, Price cannot be empty"
    assert repository.generate_errors(title="", description="some description", price_string="abc") == "Name cannot be empty, Price must be a whole number"
    assert repository.generate_errors(title="", description="some description", price_string="1.5") == "Name cannot be empty, Price must be a whole number"