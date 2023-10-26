import os
from flask import Flask, request, render_template, session, redirect, url_for
from lib.database_connection import get_flask_database_connection
from lib.user_repository import UserRepository, User
from lib.listing_repository import ListingRepository
from datetime import datetime

# Create a new Flask app
app = Flask(__name__)
app.secret_key = "secret_key" ##CHANGE THIS

# ======== ABOUT ====================== #
# About -- Project description
@app.route('/about')
def about():
    return render_template('about.html')


# ======== HOMEPAGE & SIGNING UP ====================== #

# Homepage -- Sign Up OR All Listings if User is logged in.
@app.route('/')
def homepage():
    # User in session
    if session.get('user_id') is not None:
        return redirect('/spaces') 

    else:
        return render_template('users/signup.html')

# Signup_Post -- Creating a new acc
@app.route('/', methods=['POST'])
def signup_post(): #aka create new user
    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)

    email = request.form['email']
    password1 = request.form['password1']
    password2 = request.form['password2']

    # check for errors:
    if user_repository.check_for_errors(email, password1, password2):
        return render_template('users/signup.html', errors=user_repository.generate_errors(email, password1, password2)), 400
    
    user = user_repository.create(email=email, password=password1)
    print(f"User successfully registered: {user}") #print to check if #create worked
    return redirect('/spaces') #redirect to all spaces if successful


# ======== AUTHENTICATION ROUTES ====================== #

# Login Page
@app.route('/login')
def login():
    return render_template('users/login.html')

# Login_Post
@app.route('/login', methods=['POST'])
def login_post():
    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)

    email = request.form['email']
    password = request.form['password']
    
    # login credentials match a user
    if user_repository.check_password(email=email, password_attempt=password): 
        # find user object with matching email
        user = user_repository.find_by_email(email) 
        # Set the user ID in session
        session['user_id'] = user.user_id

        # Print to check if login is successful
        print(f"app.py(79) Login successful. Session ID:{session['user_id']}")

        # Redirect to all spaces page
        return redirect('/spaces')
    
    else:
        return render_template('users/login.html', errors="Invalid username or password"), 400  

# Logging In_Get_Post: -- allows for button or hyperlink
@app.route('/signout', methods=['GET','POST'])
def signout():
    user_id = session.get('user_id')
    session.pop(user_id, None)
    print(f"app.py(90) Logout successful")

    return redirect('/login')


# ======== AUTHENTICATION-ONLY ROUTES =================== #

# # All spaces '/spaces' ['GET']
# @app.route('/spaces')
# def all_spaces_page():
#     # User in session
#     if session.get('user_id') is not None:
#         return render_template('/spaces/all_spaces.html')
#     else:
#         return redirect('/login')

# DAVE'S SECTION!!!

# # All spaces '/spaces' ['GET'] PREVIOUS
# @app.route('/spaces', methods=['GET','POST'])
# def all_spaces_page():
#     connection = get_flask_database_connection(app)
#     listing_repository = ListingRepository(connection)
#     # # User in session
#     # if session.get('user_id') is not None:
#     spaces = listing_repository.all()
#     if request.method == 'POST':
#         return render_template('/spaces/filtered_spaces.html', spaces=spaces)
#     else:
#         return render_template('/spaces/all_spaces.html', spaces=spaces)
    

# All spaces '/spaces' ['GET'] CHATGPT
@app.route('/spaces', methods=['GET', 'POST'])
def all_spaces_page():
    connection = get_flask_database_connection(app)
        # # User in session
    # if session.get('user_id') is not None:
    listing_repository = ListingRepository(connection)
    spaces = listing_repository.all()
    if request.method == 'POST':
        # Parse user-submitted dates from the form
        date_from = datetime.strptime(request.form['datefrom'], '%Y-%m-%d').date()
        date_to = datetime.strptime(request.form['dateto'], '%Y-%m-%d').date()

        # Query the 'requests' table to find available listings
        available_spaces = listing_repository.get_available_spaces(date_from, date_to)

        return render_template('/spaces/filtered_spaces.html', spaces=available_spaces)
    else:
        return render_template('/spaces/all_spaces.html', spaces=spaces)    
    # else:
    #     return redirect('/login')
    




# List a space '/spaces/new' ['GET']
## List a space_post '/spaces/new' ['POST']


# Single space page '/spaces/<id>' ['GET']
## Make a request '/spaces/<id>' ['POST']


# All requests for the session user '/requests' ['GET']
## Requests I've made, Requests I've recieved


# Single request page '/requests/<id>' ['GET']
## Confirm request '/requests/<id>/confirm' ['POST']
## Deny request '/requests/<id>/deny' ['POST']


# ===================== EXAMPLE ROUTES =================================== #
# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5000/index
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
