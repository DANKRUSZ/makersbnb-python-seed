from lib.users import User
import hashlib

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
        ## TODO: HASHING PASSWORD
        # binary_password = password.encode("utf-8")
        # hashed_password = hashlib.sha256(binary_password).hexdigest()

        query = 'INSERT INTO users (email, password) VALUES (%s, %s) RETURNING id'
        # params = [email, hashed_password]
        params = [email, password]
        rows = self._connection.execute(query, params)
        user_id = rows[0]['id']
        return user_id

    # -------- CHECKING REGISTRATION FIELDS FOR ERRORS ----------

    # Check if email is already registered to an account
    def check_for_duplicate_registration(self, email:str) -> bool:
        errors = []
        same_email_rows = self._connection.execute('SELECT id FROM users WHERE email = %s', [email])
        if same_email_rows != []:
            return True
        return False

    # Check if any errors in the form -- True if any errors:
    def check_for_errors(self, email, password1, password2):
        error_exists = False
        # Check for blank fields
        if email in ["", None] or password1 in ["", None] or password2 in ["", None]:
            error_exists = True
        # Check for duplicate emails
        if self.check_for_duplicate_registration(email=email):
            error_exists = True
        # Check for valid email
        if "@" not in email:
            error_exists = True
        # Check for length of password to be 8 chars or longer
        if len(password1) < 8:
            error_exists = True
        # Check for password and confirm password to be the same
        if password1 != password2:
            error_exists = True
        return error_exists


    def generate_errors(self, email, password1, password2) -> str:
        errors = []
        # Check for blank fields:
        if email in ["", None]:
            errors.append("Email cannot be empty")
        if password1 in ["", None]:
            errors.append("Password cannot be empty")
        # Don't need to check confirm password for blanks, it just needs to match password1
        
        # Check for duplicate email registration:
        if self.check_for_duplicate_registration(email=email) and email not in ["", None]:
            errors.append("Email is already registered")
        # Check for valid email
        if "@" not in email and email not in ["", None]:
            errors.append("Invalid email address")

        # Check for length of password to be 8 chars or longer
        if len(password1) < 8 and password1 not in ["", None]:
            errors.append("Password must be 8 chars or longer")
        # TODO: Add additional rules for password such as needing one num, one special char, one lowercase letter, one upper case letter
        # Check for password and confirm password to be the same
        if password1 != password2:
            errors.append("Confirm password must be the same as password")
        return ", ".join(errors)
    


    # == CHECK PASSWORD ============================

    # Checks password against attempt on login page.
    def check_password(self, email:str, password_attempt:str) -> bool:
        ## TODO: HASHING PASSWORD
        # binary_password_attempt = password_attempt.encode("utf-8")
        # hashed_password_attempt = hashlib.sha256(binary_password).hexidigest()
        query = 'SELECT * FROM users WHERE email = %s AND password = %s'
        # params = [email, hashed_password_attempt]
        params = [email, password_attempt]
        rows = self._connection.execute(query, params)
        if rows == []:
            return False
        return True

    def invalid_login_error(self) -> str:
        return "Invalid email and password."


    # == DELETE A USER =============

    # Delete a user by id
    def delete(self, user_id) -> None:
        query = 'DELETE FROM users WHERE id = %s'
        params = [user_id]
        self._connection.execute(query, params)
        return None
