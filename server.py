""" SafeGuard """


#########################################################################
##### Imports #####
import os

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)

from model import connect_to_db, db
from model import User, SmartCarAuth

from flask_debugtoolbar import DebugToolbarExtension

import bcrypt

# import sendgrid
# from sendgrid.helpers.mail import *

import random

import json

import smartcar

from alertingFunctions import notify_contacts_emergency, post_to_twitter, contact_lyft
from oauthRequest import o_auth2

app = Flask(__name__)

# with open('hackathon-api-key.txt') as f:
#     sendgrid_api_key = f.read().strip()

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ['APP_KEY']

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


client = smartcar.AuthClient(
    client_id=os.environ['CLIENT_ID'],
    client_secret=os.environ['CLIENT_SECRET'],
    redirect_uri='http://localhost:5000/callback',
    scope=['read_vehicle_info', 'read_location', 'read_odometer']
)

#########################################################################
##### Routes #####

@app.route('/')
def index():
    """ Homepage """
    session['user_id'] = "1"

    return render_template('homepage.html')


@app.route('/auth', methods=['GET'])
def auth():
    auth_url = client.get_auth_url(force=True)
    return '''
        <h1>Hello, Hackbright!</h1>
        <a href=%s>
          <button>Connect Car</button>
        </a>
    ''' % auth_url

@app.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code')
    access = client.exchange_code(code)

    print (access)
    response_dict = jsonify(access)


    # token = SmartCarAuth(access_token=response_dict["access_token"])

    # db.session.add(token)
    # db.session.commit()

    return response_dict

@app.route('/hi', methods=['GET'])
def auth_me():
    lyft_auth_url = o_auth2()
    return '''
        <h1>Hello, Me!</h1>
        <a href=%s>
          <button>Connect to Lyft</button>
        </a>
    ''' % lyft_auth_url


@app.route('/login-confirmation')
def login_confirm():
    """ Confirm OAuth """

    code = request.args.get('code')
    # access = client.exchange_code(code)

    print "Hello???"
    # response_dict = jsonify(access)
    return code


@app.route('/register')
def register():
    """ Registration """
    return render_template('register.html')


@app.route("/verify-registration", methods=['POST'])
def verify_registration():
    """ Verify registration form """

    print "User Registration"

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")


    # Hash the password because security is important
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    print "First:", first_name
    print "Last:", last_name
    print "Email:", email
    print "PW:", hashed_pw

    # Look for the email in the DB
    existing_user = User.query.filter(User.email == email).all()

    if len(existing_user) == 0:


        print "New User"
        user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_pw)
        print user

        db.session.add(user)
        db.session.commit()

        flash("You are now registered!")
        return redirect('/profile')

    elif len(existing_user) == 1:
        print "Existing user"
        flash("You're already registered!")
        return redirect('/')

    else:
        print "MAJOR PROBLEM!"
        flash("You have found a website loophole... Please try again later.")
        return redirect("/")



@app.route('/profile')
def profile():
    """Show profile
    """
    return render_template('profile.html')


@app.route('/log_in')
def log_in():
    """Allows user to log in
    """
    return render_template('log_in.html')

@app.route("/log_out")
def log_out():
    """allow user to log out of Givr."""
    session.clear()

    return redirect("/")

@app.route('/log_in', methods=["POST"])
def log_me_in():

    login_email = request.form.get("email")
    login_password = request.form.get("password")

    print login_email, login_password

    # Get user object
    existing_user = User.query.filter(User.email == login_email).all()

    # In DB?
    if len(existing_user) == 1:
        print "Email in DB"
        existing_password = existing_user[0].password

        # Correct password (hashed)?
        if bcrypt.hashpw(login_password.encode('utf-8'), existing_password.encode('utf-8')) == existing_password:
            if 'login' in session:
                flash("You are already logged in!")
                return redirect('/')
            else:
                #Add to session
                session['user_id'] = existing_user[0].user_id
                flash("Hi {}, you are now logged in!".format(existing_user[0].first_name))
                return redirect('/')
        else:
            flash("Incorrect password. Please try again.")
            return redirect('/log_in')

    # Not in DB
    elif len(existing_user) == 0:
        print "Email not in DB"
        flash("That email couldn't be found. Please try again.")
        return redirect('/log_in')

    else:
        print "MAJOR PROBLEM!"
        flash("You have found a website loophole... Please try again later.")
        return redirect("/")


def create_user(email, password):
    return "1"

@app.route('/emergency-contacts')
def emergency_contacts():
    """Returns a page where the user can configure emergency contacts
    """
    return render_template('emergency-contacts.html')


@app.route('/add-emergency-contact')
def add_emergency_contacts():
    """A user clicks add contact and this stores it to the db and returns a success message
    """

    #Parse request objects
    #Store to the db
    #return a success using AJAX

    return "Contact successfully added!"

@app.route('/emergency-mode')
def emergency_mode():
    """User is in dire danger and presses emergency mode button which fires off alerts to contacts, twitter and lyft. 
    Also unlocks the doors of the vehicle
    """

    rider = "Jade Paoletta" #hardcoded, but should be pulled from user profile
    #Call Lyft API to get info about the driver's car, store in object

    #Text contacts, this should eventually take argument of user info
    notify_contacts_emergency(rider) 

    #Post to twitter

    #Contact Lyft

    #Unlock the doors

    flash("Emergency Mode has been activated! Try to get away from the situation and to safety")
    return redirect("/")


@app.route('/sendemail')
def send():
    sendemail("""
        <html>
            <head>
            </head>
            <body>
                <h1>Sent from Python</h1>
                I like python.
            </body>
        </html>
    """)
    return "ok"

def sendemail(recipient, alertbody):
    print("SENDING EMAIL TO", recipient, "BODY", alertbody)
    sg = sendgrid.SendGridAPIClient(apikey=sendgrid_api_key)
    from_email = Email("davidvgalbraith@gmail.com")
    to_email = Email(recipient)
    subject = "Message from Circlet"
    content = Content("text/html", alertbody)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print("SEND EMAIL RESPONSE")
    print(response.status_code)
    print(response.body)
    print(response.headers)

def make_recipient():
    """Instantiating a new Recipient """
    print "Getting ready to instantiate a new recipient"


    address = actual_destination.rstrip()

    address, city, N = row.split(",")
    state, zipcode = N.split(" ")

    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=address,+city+state,+zipcode')

    resp_json_payload = response.json()

    print(resp_json_payload['results'][0]['geometry']['location'])


    recipient = Recipient(recipient_id=recipient_id,
                          address=address,
                          city=city,
                          state=state,
                          zipcode=zipcode,
                          latitude=latitude,
                          longitude=longitude,
                          recipient_type=recipient_type)


    # Flash success message or redirct user
    db.session.add(giv)
    db.session.commit()


@app.route("/rapid_small_giv", methods=['POST', 'GET'])
def rapid_giv():
    """allow user to complete a giv."""

    email = session["email"]
    user = Givr.query.filter_by(email=email).first()
    fname = user.fname
    giv_amount = user.smallgiv
    session["giv_amount"] = giv_amount
    # giv_size = request.args.get("smallgiv")


    famous_inventors = ["Thomas L. Jennings", "Mark E. Dean", "Madam C.J. Walker", "Dr. Shirely Jackson",
                        "Charles Richard Dew", "Marie Van Brittan Brown", "George Carruthers", "Dr. Patricia Bath",
                        "Jan E. Matzeliger", "Alexander Miles"]

    if request.method == "POST":
        # Get Form Data (giv_size and address)


        address = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        zipcode = request.form.get("zipcode")

        full_address = "{}, {}, {} {}".format(address, city, state, zipcode)
        print "full_address: ", full_address
        pickup_notes = "Please make sure that the order includes eating utensils and napkins."
        dropoff_notes = "Please deliver to visibly homeless individual in front of addresss or very close to address. "

        closest_restaurant = find_closest_restaurant()
        print "*****************************closest_restaurant: \n"
        print type(closest_restaurant)
        print closest_restaurant

        best_match_name, best_price_match = find_match_name(closest_restaurant, giv_amount)

        ################################# Create postmates request
        #Delivery Quotes
        payload = {"dropoff_address": full_address,
                   "pickup_address": closest_restaurant.address}

        print "payload: ", payload

        response_from_postmates = requests.post("https://api.postmates.com/v1/customers/cus_Lk1phJYn_uU88V/delivery_quotes", data=payload, auth=("a03e8608-cf6b-4441-ade2-696e2c437d6c", ''))
        response_from_postmates_dictionary = response_from_postmates.json()
        print
        pprint(response_from_postmates_dictionary)
        print
        print response_from_postmates_dictionary['currency']
        quote_id = response_from_postmates_dictionary['id']

        ################################# Create postmates request
        #Create a Delivery
        payload_delivery = {"quote_id": quote_id,
                            "manifest": best_match_name,
                            "manifest_reference": random.choice(famous_inventors) + " " + quote_id, #how to auto increment the order number?
                            "pickup_name": closest_restaurant.name,
                            "pickup_address": closest_restaurant.address,
                            "pickup_phone_number": "510-866-4577",
                            "pickup_business_name": closest_restaurant.name,
                            "pickup_notes": pickup_notes,
                            "dropoff_name": "unknown",
                            "dropoff_address": full_address,
                            "dropoff_phone_number": "888-712-9985",
                            "dropoff_business_name": "N/A",
                            "dropoff_notes": dropoff_notes,
                            "requires_id": "false",
                            }
        print "payload_delivery: ", payload_delivery

        #all of this needs updating
        response_from_postmates_delivery = requests.post("https://api.postmates.com/v1/customers/cus_Lk1phJYn_uU88V/deliveries", data=payload_delivery, auth=("a03e8608-cf6b-4441-ade2-696e2c437d6c", ''))
        response_from_postmates_dictionary = response_from_postmates_delivery.json()
        print
        pprint(response_from_postmates_dictionary)
        print

        """Instantiating a new giv """
        print "Getting ready to instantiate a new giv"

        manifest_reference = payload_delivery["manifest_reference"]
        tracking_url = response_from_postmates_dictionary["tracking_url"]
        date_of_order = response_from_postmates_dictionary["created"]
        date_of_delivery = response_from_postmates_dictionary["dropoff_eta"]
        requested_destination = payload_delivery["dropoff_address"]
        actual_destination = payload_delivery["dropoff_address"]
        total_amount = best_price_match
        successful_delivery = True
        # recipient_id =
        size = "small"
        tax_exempt = False
        restaurant = Restaurant.query.filter_by(name=closest_restaurant.name).first()
        print restaurant.restaurant_id

        giv = Giv(givr_id=user.givr_id,
                  restaurant_id=restaurant.restaurant_id,
                  date_of_order=date_of_order,
                  date_of_delivery=date_of_delivery,
                  requested_destination=requested_destination,
                  actual_destination=actual_destination,
                  total_amount=total_amount,
                  successful_delivery=successful_delivery,
                  size=size,
                  tax_exempt=tax_exempt)

        print "I am date_of_order", date_of_order
        print "I am date_of_delivery", date_of_delivery
        print "I am requested_destination", requested_destination
        print "I am actual_destination", actual_destination
        print "I am total_amount", total_amount
        print "I am successful_delivery", successful_delivery,
        print "I am size", size
        print "I am tax_exempt", tax_exempt

        db.session.add(giv)
        db.session.commit()

        print "We created a new Giv!"

        flash("You have successfully created a delivery.")

        """Instantiating a new Recipient """
        print "Getting ready to instantiate a new recipient"

        recipient = Recipient.query.order_by('-recipient_id').first()


        print "in recipient for loop"
        address = actual_destination
        print "assigned address to actual_destination"
        address, city, state_zip = address.split(",")
        print "successfully split address, city, state_zip"
        print "This is state_zip", state_zip

        state = state_zip[:-6]
        zipcode = state_zip[-5:]

        print "separated state and zip"

        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=address,+city+state,+zipcode')

        resp_json_payload = response.json()

        google_location_dictionary = (resp_json_payload['results'][0]['geometry']['location'])

        latitude = google_location_dictionary["lat"]
        print "I am latitude", latitude

        longitude = google_location_dictionary["lng"]
        print "I am longitude", longitude

        if tax_exempt == True:
            recipient_type = "organization"
        else:
            recipient_type = "individual"

        print "This is recipient_type", recipient_type

        recipient_id = recipient.recipient_id + 1

        recipient = Recipient(recipient_id=recipient_id,
                              address=address,
                              city=city,
                              state=state,
                              zipcode=zipcode,
                              latitude=latitude,
                              longitude=longitude,
                              recipient_type=recipient_type)

        print "This is address, city, state, zipcode", address, city, state, zipcode


        # Flash success message or redirct user
        db.session.add(recipient)
        db.session.commit()

        return render_template("track_order.html", manifest_reference=manifest_reference,
                               fname=fname, tracking_url=tracking_url)

    return render_template("rapid_small_giv.html")


@app.route('/location_warning')
def map_test():
    

    json_data = open('sample_directions.json').read()
    data = json.loads(json_data)
    current_location = data['routes'][0]['legs']

    return render_template('location_warning.html',
                           current_location=current_location)



#########################################################################
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
