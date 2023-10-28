import os
from flask import Flask, request, render_template, session, redirect, url_for
from lib.database_connection import get_flask_database_connection
from lib.user_repository import UserRepository
from lib.listing_repository import ListingRepository
from lib.date_listing_repo import DateListingRepo
from lib.request_repository import RequestRepository
from datetime import datetime, timedelta

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
    
    #CAPTURING FORM SUBMISSION FIELDS:
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
    # User in session
    if session.get('user_id') is not None:
        return redirect('/spaces') 

    else:
        return render_template('users/login.html')

# Login_Post
@app.route('/login', methods=['POST'])
def login_post():
    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)

    #CAPTURING FORM SUBMISSION FIELDS:
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
    # Clear the user_id from the session
    session.pop('user_id', None)

    # Redirect to the root URL or any desired URL after logout
    return redirect('/')


# ======== AUTHENTICATION-ONLY ROUTES =================== #

# ======== ALL SPACES, LIST A SPACE & INDIVIDUAL SPACE ROUTES =================== #

#TODO - the issue seems to be that the dates are not being successfully sumbitted to the SQL query. :-(
@app.route('/spaces', methods=['GET','POST'])
def all_spaces_page():
    # User in session
    if session.get('user_id') is not None:
        connection = get_flask_database_connection(app)
        listing_repository = ListingRepository(connection)    
        spaces = listing_repository.all()

        if request.method == 'POST':
            date_from_string = request.form['date_from']
            date_to_string = request.form['date_to']
            print(f"Date from: {date_from_string}, Date to: {date_to_string}")
            #TODO: error handling for blank fields or when date is invalid;



            date_from = datetime.strptime(date_from_string, '%Y-%m-%d')
            date_to = datetime.strptime(date_to_string, '%Y-%m-%d')
            available_spaces = listing_repository.find_available_listings_for_dates(available_from=date_from, available_to=date_to)
            return render_template('/spaces/all_spaces.html', spaces=available_spaces)
        else:
            return render_template('/spaces/all_spaces.html', spaces=spaces)
    else:
        return redirect('/login')   



# List a space '/spaces/new' ['GET']
@app.route('/spaces/new')
def list_a_space_page():
    # User in session
    if session.get('user_id') is not None:
        return render_template('spaces/list_a_space.html')
    else:
        return redirect('/login')

# List a space_post '/spaces/new' ['POST']
@app.route('/spaces/new', methods=['POST'])
def list_a_space_post():
    #aka create new listing
    connection = get_flask_database_connection(app)
    listing_repository = ListingRepository(connection)
    availability_repository = DateListingRepo(connection)

    #CAPTURING FORM SUBMISSION FIELDS:
    #listing
    title = request.form['name'] #cannot be blank
    title = title.title() #convert to title case
    description = request.form['description'] #cannot be blank
    price_string = request.form['price'] #must be numeric -- integer, not float or non-number

    #availability
    available_from_string = request.form['available_from'] #cannot be blank, must be on or after today
    available_to_string = request.form['available_to'] #cannot be blank, must be on or after available_from

    #owner_id
    owner_id = session.get('user_id')

    # check for errors:
    # Errors listed above in fields.
    if listing_repository.check_for_errors(title, description, price_string) and availability_repository.check_for_errors_new_listing(available_from_string, available_to_string):
        return render_template(
            'spaces/list_a_space.html', 
            listing_errors=listing_repository.generate_errors(title, description, price_string), 
            availability_errors=availability_repository.generate_errors_new_listing(available_from_string, available_to_string)
            ), 400
    elif listing_repository.check_for_errors(title, description, price_string):
        return render_template(
            'spaces/list_a_space.html', 
            listing_errors=listing_repository.generate_errors(title, description, price_string)
            ), 400
    elif availability_repository.check_for_errors_new_listing(available_from_string, available_to_string):
        return render_template(
            'spaces/list_a_space.html', 
            availability_errors=availability_repository.generate_errors_new_listing(available_from_string, available_to_string)
            ), 400

    #convert strings to datetime objects
    available_from = datetime.strptime(available_from_string, '%Y-%m-%d') #error handling for blanks and invalid date is handled above
    available_to = datetime.strptime(available_to_string, '%Y-%m-%d') #error handling for blanks and invalid date is handled above
    
    #convert price to integer
    price = int(price_string) #error handling for float or non-numeric is handled above.

    #listing
    listing_id = listing_repository.create(title=title, description=description, price=price, owner_id=owner_id)
    print(f"Space successfully listed: #{listing_id}") #print to check if #create worked

    #availability -- make a new available date for the new listing for each date in the date range, inclusive
    new_availability_date = available_from
    while new_availability_date <= available_to:
        new_availability_id = availability_repository.create(date_available=new_availability_date, listing_id=listing_id, request_id=None)
        print(f"New availability date for listing {listing_id}, id: {new_availability_id}, date:{new_availability_date}")
        new_availability_date += timedelta(days=1)
    
    return redirect(f'/spaces/{listing_id}') #redirect to the new listing's page



# Single space page '/spaces/<id>' ['GET']
@app.route('/spaces/<int:id>')
def single_space_page(id):
    # User in session
    if session.get('user_id') is not None:
        #get the listing object 
        connection = get_flask_database_connection(app)
        listing_repository = ListingRepository(connection)
        listing = listing_repository.find(id)
        availability_repository = DateListingRepo(connection)

        #get all availabilities for this listing:
        all_available_dates = availability_repository.find_availabilities(listing_id=listing.id)
        print(all_available_dates)

        #get all the booked dates for the listing
        booked_dates = [date['date'] for date in all_available_dates if date['request_id'] != None]
        print(booked_dates)

        #find all free dates for the listing
        free_dates = [date['date'] for date in all_available_dates if date['request_id'] == None]
        print(free_dates)


        return render_template('spaces/show_space2.html', listing=listing, free_dates=free_dates, booked_dates=booked_dates)
    else:
        return redirect('/login')


# ======== ALL REQUESTS, MAKER A REQUEST & INDIVIDUAL REQUEST ROUTES =================== #

## Make a request '/spaces/<id>' ['POST']
@app.route('/spaces/<int:id>', methods=['POST'])
def single_space_post_booking_request(id):
    connection = get_flask_database_connection(app)
    repository = RequestRepository(connection)

    #Get requested date & convert to datetime object
    date_string = request.form['selected_date']
    print(date_string)
    date = datetime.strptime(date_string, '%Y-%m-%d')

    #Get session users's id
    requester_id = session.get('user_id')

    #Create new request
    request_id = repository.create(date_requested=date, listing_id=id, requester_id=requester_id, confirmed=None)
    
    return redirect(f'/requests/{request_id}')


# All requests for the session user '/requests' ['GET']
## Requests I've made, Requests I've recieved
@app.route('/requests', methods=['GET'])
def get_requests():
    connection = get_flask_database_connection(app)
    repository = RequestRepository(connection)

    requester_id = session.get('user_id')
    owner_id = session.get('user_id')
    requests_made = repository.requests_made(requester_id)
    requests_received = repository.requests_received(owner_id)

    return render_template('requests/requests.html', requests_made=requests_made, requests_received=requests_received)

# Single request page '/requests/<id>' ['GET']
@app.route('/requests/<int:id>')
def single_request_get(id):
    connection = get_flask_database_connection(app)
    repository = RequestRepository(connection)
    session_user = session.get('user_id')

    # IF SESSION USER OWNS THIS LISTING
    if repository.check_if_owned_by(request_id=id, user_id=session_user):
        
        # Get extended dictionary for this request, including listing_id, title, description
        request_dict = repository.find_extended_details_for_request(request_id=id)
        # Find the requester's email from their user_id. Add this to the request_dict
        requester_email = repository.find_email_for_user(user_id=request_dict["requester_id"])
        request_dict["requester_email"] = requester_email

        # Find the details of the other requests, and format as cards on render template
        other_requests = repository.find_other_requests(request_id=id)

        return render_template('requests/single_request_owner.html', this_request=request_dict, other_requests=other_requests)

    # IF SESSION USER DOES NOT OWN THIS LISTING
    else:
        # Get extended dictionary for this request, including listing_id, title, description
        request_dict = repository.find_extended_details_for_request(request_id=id)

        # Find the owner's email from their user_id. Add this to the request_dict
        owner_email = repository.find_email_for_user(user_id=request_dict["owner_id"])
        request_dict["owner_email"] = owner_email

        return render_template('requests/single_request.html', this_request=request_dict)

## Confirm request
@app.route('/requests/<id>/confirm', methods=['POST'])
def single_request_confirm_post(id):
    ## @Daniel @Dave
    # Should update the 'confirmed' column for requests to TRUE for WHERE requests.id = id
    # Should update the 'request_id' column for dates_listings to id for WHERE listing_id =%s AND date_available =%s' [list_id of the request, date_requested of the request]
    # should return redirect('/requests')
    choice = f"Confirm request #{id}"
    return choice
    

## Deny request
@app.route('/requests/<id>/deny', methods=['POST'])
def single_request_deny_post(id):
    ## @Daniel @Dave
    # Should update the 'confirmed' column for requests to FALSE for WHERE requests.id = id
    # should return redirect('/requests')
    choice = f"Deny request #{id}"
    return choice





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
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
