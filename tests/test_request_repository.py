from datetime import date
from lib.request_repository import RequestRepository
from lib.request import Request

## Requests REPOSITORY ###########

# ==== ALL =========== #######
def test_all(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = RequestRepository(db_connection)

    assert repository.all() == [
        Request(1, date(2023,10,24), 1, 3, True),
        Request(2, date(2023,10,24), 2, 1, None),
        Request(3, date(2023,10,24), 3, 2, None),
        Request(4, date(2023,10,24), 4, 1, None)
    ]

# ====== FIND ========== #
def test_find(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = RequestRepository(db_connection)

    assert repository.find(3) == Request(3, date(2023,10,24), 3, 2, None)
    assert repository.find(5) == None

def test_find_by_requseter_id(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = RequestRepository(db_connection)

    assert repository.find_by_requester_id(1) == [Request(2, date(2023,10,24), 2, 1, None), Request(4, date(2023,10,24), 4, 1, None)]
    assert repository.find_by_requester_id(5) == []


# ======= CREATE ======= #
def test_create(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = RequestRepository(db_connection)

    assert repository.create(date(2023,10,23), 4, 3, None) == 5
    assert repository.all() == [
        Request(1, date(2023,10,24), 1, 3, True),
        Request(2, date(2023,10,24), 2, 1, None),
        Request(3, date(2023,10,24), 3, 2, None),
        Request(4, date(2023,10,24), 4, 1, None),
        Request(5, date(2023,10,23), 4, 3, None)
        ]
    


# ======= DELETE ======= #
def test_delete_request(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = RequestRepository(db_connection)

    repository.delete(1)
    assert repository.all() == [
        Request(2, date(2023,10,24), 2, 1, None),
        Request(3, date(2023,10,24), 3, 2, None),
        Request(4, date(2023,10,24), 4, 1, None)
    ]

# ===== CONFIRM A REQUEST =====

def test_confirm_request(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = RequestRepository(db_connection)

    repository.confirm(2)
    assert sorted(repository.all(), key=lambda x: x.id) == [
        Request(1, date(2023,10,24), 1, 3, True),
        Request(2, date(2023,10,24), 2, 1, True),
        Request(3, date(2023,10,24), 3, 2, None),
        Request(4, date(2023,10,24), 4, 1, None)
    ]


    # ===== DENY A REQUEST =====

def test_deny_request(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = RequestRepository(db_connection)

    repository.deny(1)
    assert sorted(repository.all(), key=lambda x: x.id) == [
        Request(1, date(2023,10,24), 1, 3, False),
        Request(2, date(2023,10,24), 2, 1, None),
        Request(3, date(2023,10,24), 3, 2, None),
        Request(4, date(2023,10,24), 4, 1, None)
    ]