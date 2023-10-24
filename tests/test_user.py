from lib.users import User
from datetime import datetime

## USER CLASS ####

def test_user_eq():
    user1 = User(1, "test_email@gmail.com", "this9ISaSTRONGp@@@Sword")
    user2 = User(1, "test_email@gmail.com", "this9ISaSTRONGp@@@Sword")
    assert user1 == user2

def test_user_repr():
    user1 = User(1, "test_email@gmail.com", "this9ISaSTRONGp@@@Sword")
    assert str(user1) == "User(1, Email:test_email@gmail.com)"