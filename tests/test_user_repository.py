from lib.user_repository import User, UserRepository

## USER REPOSITORY ###########

# ==== ALL =========== #######
def test_all(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = UserRepository(db_connection)

    assert repository.all() == [
        User(1, 'dan@email.com', 'password'),
        User(2, 'dave@email.com', 'lastword'),
        User(3, 'claire@email.com', 'passstone'),
        User(4, 'onuora@email.com', 'passroad')
    ]

# ====== FIND ========== #
def test_find(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = UserRepository(db_connection)

    assert repository.find(3) == User(3, 'claire@email.com', 'passstone')
    assert repository.find(5) == None

def test_find_by_email(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = UserRepository(db_connection)

    assert repository.find_by_email("dan@email.com") == User(1, 'dan@email.com', 'password')
    assert repository.find_by_email('notauser@gmail.com') == None

# ======= CREATE ======= #
def test_create(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = UserRepository(db_connection)

    assert repository.create("test_email@gmail.com", "this9ISaSTRONGp@@@Sword") == 5
    assert repository.all() == [
        User(1, 'dan@email.com', 'password'),
        User(2, 'dave@email.com', 'lastword'),
        User(3, 'claire@email.com', 'passstone'),
        User(4, 'onuora@email.com', 'passroad'),
        User(5, "test_email@gmail.com", "this9ISaSTRONGp@@@Sword")
    ]

# ------- FORM CHECK ERRORS FOR CREATE -------------- #
def test_check_registration_duplicate(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = UserRepository(db_connection)

    assert repository.check_for_duplicate_registration("notarepeatemail@gmail.com") == []
    assert repository.check_for_duplicate_registration("dan@email.com") == ["Email is already registered with an account"]

def test_is_valid(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = UserRepository(db_connection)

    assert repository.is_valid("", "") == ["Email cannot be empty", "Password cannot be empty"]
    assert repository.is_valid("notavalidemail", "pw2short") == ["Invalid email address", "Password must be 8 chars or longer"]

def test_generate_errors(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = UserRepository(db_connection)

    assert repository.generate_errors([]) == None

def test_delete_user(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = UserRepository(db_connection)

    repository.delete(1)
    assert repository.all() == [
        User(2, 'dave@email.com', 'lastword'),
        User(3, 'claire@email.com', 'passstone'),
        User(4, 'onuora@email.com', 'passroad')
    ]