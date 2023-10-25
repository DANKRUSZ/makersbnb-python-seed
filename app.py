import os
from flask import Flask, request, render_template, session, redirect
from lib.database_connection import get_flask_database_connection
from lib.user_repository import UserRepository, User


# Create a new Flask app
app = Flask(__name__)

# ======== ABOUT ====================== #
# About -- Project description
@app.route('/about')
def about():
    return render_template('about.html')


# ======== HOMEPAGE & SIGNING UP ====================== #

# TODO: Claire - TESTING
# Homepage -- Sign Up OR All Listings if User is logged in.
@app.route('/')
def homepage():
    # user is not loggedin
    if 'user_id' not in session:
        return render_template('users/signup.html')

    # redirect to all spaces if user is logged in
    else:
        return redirect('/spaces') 

# Signup_Post -- Creating a new acc
@app.route('/', methods=['POST'])
def signup_post(): #aka create new user
    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)

    email = request.form['email']
    password1 = request.form['password1']
    password2 = request.form['password2']

    # CHECK FOR ENTRY FIELDS VALIDITY: ####

    # check for errors:
    if user_repository.check_for_errors(email, password1, password2):
        return render_template('users/signup.html', errors=user_repository.generate_errors(email, password1, password2)), 400
    

    user = user_repository.create(email=email, password=password1)
    print(f"User successfully registered: {user}") #print to check if #create worked
    return redirect('/spaces') #redirect to all spaces if successful


# ======== AUTHENTICATION ROUTES ====================== #

# TODO: Claire - write & test
# Login Page
@app.route('/login')
def login():
    return "TODO!"
    # return render_template('login.html')

# Login_Post
@app.route('/login', methods=['POST'])
def login_post():
    # NOTE by Claire: commenting out the below, as my playwright needs a different syntax. Not sure if this is the same for everyone
    email = request.form['email']
    password = request.form['password']

    # login credentials match a user
    if UserRepository.check_password(email, password): 
        # find user object with matching email
        user = UserRepository.find_by_email(email) 
        # Set the user ID in session
        session['user_id'] = user.user_id

        # Print to check if login is successful
        print(f"Login successful. Session ID:{session['user_id']}")

        # Redirect to all spaces page
        return redirect('/spaces')
    
    else:
        return render_template('users/login.html', errors="Invalid username or password"), 400  ##TODO change this



# ======== AUTHENTICATION-ONLY ROUTES =================== #

# All spaces '/spaces' ['GET']
@app.route('/spaces')
def all_spaces_page():
    if 'user_id' not in session:
        # No user id in the session so the user is not logged in.
        return redirect('/login')
    else:
        # The user is logged in, display their account page.
        return render_template('/spaces/all_spaces.html')
    


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
