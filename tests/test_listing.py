from lib.listing import *

'''
Test constructor
'''
def test_listing_constructs():
    listing = Listing(1, 1, 'House1', 'House_description1', 10)
    assert listing.id == 1
    assert listing.owner_id == 1
    assert listing.title == 'House1'
    assert listing.description == 'House_description1'
    assert listing.price == 10


'''
Testing equality
'''

def test_listings_are_equal():
    listing1 = Listing(2, 2, 'House2', 'House_description2', 12)
    listing2 = Listing(2, 2, 'House2', 'House_description2', 12)
    assert listing1 == listing2


    '''
    Testing format
    '''
def test_format():
    listing1 = Listing(2, 2, 'House2', 'House_description2', 12)
    result = listing1.format()
    assert result == 'ID: 2, User: 2, Title: House2, Description: House_description2, Price: £12'