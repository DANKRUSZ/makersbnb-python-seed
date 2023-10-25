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

    #TODO Import hashlib and test with encrypted pass.

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

    assert repository.check_for_duplicate_registration("notarepeatemail@gmail.com") == False
    assert repository.check_for_duplicate_registration("dan@email.com") == True

def test_check_for_errors(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = UserRepository(db_connection)

    assert repository.check_for_errors(email="", password1="", password2="") == True
    assert repository.check_for_errors(email="notanemail", password1="blahblah", password2="blahblah") == True
    assert repository.check_for_errors(email="dan@email.com", password1="blahblah", password2="blahblah") == True
    assert repository.check_for_errors(email="new_user@test.com", password1="blahblahblah", password2="notamatch") == True
    assert repository.check_for_errors(email="new_user@test.com", password1="tooshrt", password2="blahblahblah") == True


def test_generate_errors(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = UserRepository(db_connection)
    assert repository.generate_errors(email="", password1="", password2="") == "Email cannot be empty, Password cannot be empty"
    assert repository.generate_errors(email="notanemail", password1="blahblah", password2="blahblah") == "Invalid email address"
    assert repository.generate_errors(email="dan@email.com", password1="blahblah", password2="blahb") == "Email is already registered, Confirm password must be the same as password"
    assert repository.generate_errors(email="new_user@test.com", password1="tooshrt", password2="tooshrt") == "Password must be 8 chars or longer"

def test_delete_user(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = UserRepository(db_connection)

    repository.delete(1)
    assert repository.all() == [
        User(2, 'dave@email.com', 'lastword'),
        User(3, 'claire@email.com', 'passstone'),
        User(4, 'onuora@email.com', 'passroad')
    ]

# ======= LOGIN CREDENTIALS CHECK ========================

#TODO Import hashlib and test with encrypted pass.

def test_check_password(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = UserRepository(db_connection)

    assert repository.check_password("dan@email.com", "password") == True
    assert repository.check_password("dan@email.com", "woijoih") == False
