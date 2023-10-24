class User:

    def __init__(self, user_id:int, email:str, password:str) -> None:
        self.user_id = user_id
        self.email = email
        self.password = password

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return self.__dict__ == other.__dict__
    
    def __repr__(self) -> str:
        return f"User({self.user_id}, Email:{self.email})"
