from lib.listing import *

'''
Test constructor
'''
def test_listing_constructs():
    listing = Listing(1, 'House1', 'House_description1', 100, 1)
    assert listing.id == 1
    assert listing.owner_id == 1
    assert listing.title == 'House1'
    assert listing.description == 'House_description1'
    assert listing.price == 100


'''
Testing equality
'''

def test_listings_are_equal():
    listing1 = Listing(1, 'House1', 'House_description1', 100, 1)
    listing2 = Listing(1, 'House1', 'House_description1', 100, 1)
    assert listing1 == listing2


    '''
    Testing format
    '''
def test_format():
    listing = Listing(1, 'House1', 'House_description1', 100, 1)
    result = listing.format()
    assert result == 'ID: 1, Owner_ID: 1, Title: House1, Description: House_description1, Price: £100'