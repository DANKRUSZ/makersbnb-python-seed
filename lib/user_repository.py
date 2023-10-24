from lib.users import User

class UserRepository:
    def __init__(self, connection):
        self._connection = connection
    
    # generate multiple users from SQL query rows
    def generate_users(self, rows) -> list[User]:
        users = []
        for row in rows:
            user = User(row['id'], row['email'], row['password'])
            users.append(user)
        return users
    
    # generate a single user from a SQL query row
    def generate_single_user(self, rows) -> User:
        if rows == []:
            return None
        row = rows[0]
        return User(row['id'], row['email'], row['password'])

    # == ALL USERS ===
    # Retrieve all registered users from db
    def all(self) -> list[User]:
        query = 'SELECT * FROM users'
        rows = self._connection.execute(query)
        return self.generate_users(rows)

    # == FIND SINGLE USER =============
    # Find a single user by id
    def find(self, user_id:int) -> User:
        query = 'SELECT * FROM users WHERE id=%s'
        params = [user_id]

        rows = self._connection.execute(query, params)
        return self.generate_single_user(rows)
    
    # Find a single user by email -- one unique email for each user in the db
    def find_by_email(self, email:str) -> User or None:
        query = 'SELECT * FROM users WHERE email=%s'
        params = [email]

        rows = self._connection.execute(query, params)
        return self.generate_single_user(rows)



    # == CREATE NEW USER & ERRORS =============

    # Create a new user, returning user id
    # NOTE using create with fields instead of User object for ease of error handling.
    def create(self, email:str, password:str) -> int:
        query = 'INSERT INTO users (email, password) VALUES (%s, %s) RETURNING id'
        params = [email, password]
        rows = self._connection.execute(query, params)
        user_id = rows[0]['id']
        return user_id

    # Check for duplicate email
    def check_for_duplicate_registration(self, email:str) -> list:
        errors = []
        same_email_rows = self._connection.execute('SELECT id FROM users WHERE email = %s', [email])
        if same_email_rows != []:
            errors.append("Email is already registered with an account")
        return errors

    # Check if fields for creating a new user are valid
    def is_valid(self, email:str, password:str) -> list:
        errors = []
        if email == None or email == "":
            errors.append("Email cannot be empty")
        elif "@" not in email: #TODO Refine this!
            errors.append("Invalid email address")

        if password == None or password == "":
            errors.append("Password cannot be empty")
        elif len(password) <= 8:
            errors.append("Password must be 8 chars or longer")
        # TODO: Add additional rules for password such as needing one num, one special char, one lowercase letter, one upper case letter
        return errors

    # Generate errors as a string #TODO add additional errors lists here such as password lenght, etc
    def generate_errors(self, is_valid_errors) -> None or str:
        if is_valid_errors == []:
            return None
        return ", ".join(is_valid_errors)


    # == DELETE A USER =============

    # Delete a user by id
    def delete(self, user_id) -> None:
        query = 'DELETE FROM users WHERE id = %s'
        params = [user_id]
        self._connection.execute(query, params)
        return None
