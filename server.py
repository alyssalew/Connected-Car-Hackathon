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


from requests.auth import HTTPBasicAuth
from alertingFunctions import notify_contacts_emergency, post_to_twitter, contact_lyft
from oauthRequest import retrieve_access_token

#### Comment out to run server to re-generate SmartCar Access Token ####
import smartcarRequest

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
    test_mode='test',
    scope=['read_vehicle_info', 'read_location', 'read_odometer','control_security', 'control_security:unlock', 'control_security:lock']
)

#########################################################################
##### Routes #####

##### Auth SmartCar [To be put on driver-side] #####
@app.route('/auth', methods=['GET'])
def auth():
    auth_url = client.get_auth_url(force=True)
    return '''
        <h1>Hello!</h1>
        <h2>This app would like access to your car(s). Please click the button to connect. </h2>
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

    # Store token in session
    session['access_token'] = access['access_token']
    access_token = session['access_token']

    print "This is the token:", access_token

    return '''
        <h2> Thank you for giving access to your car(s)! </h2>
    '''

    # return code


####### Rider-side routes #######
@app.route('/')
def homepage():
    """ Homepage """

    session['user_id'] = "1"
    return render_template('homepage.html')

@app.route('/log_in')
def log_in():
    """Allows user to log in """
    return render_template('log_in.html')

@app.route("/log_out")
def log_out():
    """allow user to log out """
    session.clear()

    return redirect("/")

@app.route('/login_confirmation')
def login_confirmation():
    """confirms once the user has loggedin"""

    code = request.args.get("code")
    print code

    results = retrieve_access_token(code)
    print results

    return redirect("/ride_details")

@app.route('/ride_details')
def ride_details():
    """ Homepage """
    # session['user_id'] = "1"

    return render_template('ride_details.html')


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

@app.route('/emergency_mode')
def emergency_mode_template():
    """ Renders Emergency Mode in MockUp 3"""

    return render_template('emergency_mode.html')

@app.route('/activate-emergency-mode')
def activate():
    """User is in dire danger and presses emergency mode button which fires off alerts to contacts, twitter and lyft. 
    Also unlocks the doors of the vehicle
    """
    access_token = session.get('access_token')
    print access_token

    # Get vehicle object
    vehicle = smartcarRequest.get_a_vehicle(access_token)

    # Get vehicle info
    vehicle_info = smartcarRequest.get_vehicle_info(vehicle)

    #Text contacts, this should eventually take argument of user info
    rider = "Jade Paoletta" #hardcoded, but should be pulled from user profile

    ########## Comment out to turn off text notifications! ##############
    # notify_contacts_emergency(rider)

    #Get location of the car
    location = smartcarRequest.get_location(vehicle)
    coordiates = smartcarRequest.get_coordiates(location)

    #Post to twitter

    #Contact Lyft

    #Unlock the doors
    # print smartcarRequest.unlock_car(smartcarRequest.vehicle)
    ## NEED TO FAKE UNLOCKING CAR

    return render_template('emergency-confirmed.html', vehicle_info=vehicle_info, coordiates=coordiates)


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

@app.route("/destination_warning", methods=['POST', 'GET'])
def destination_warning():
    """get Google API to work"""

    """Instantiating a new Recipient """
    print "Getting ready to instantiate a new recipient"

    address = "833 Calmar Avenue"
    city = "Oakland"
    state = "CA"
    zipcode = "94610"


    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=address,+city+state,+zipcode')

    resp_json_payload = response.json()

    print(resp_json_payload['results'][0]['geometry']['location'])

    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=address,+city+state,+zipcode')

    resp_json_payload = response.json()

    google_location_dictionary = (resp_json_payload['results'][0]['geometry']['location'])

    latitude = google_location_dictionary["lat"]
    print "I am latitude", latitude

    longitude = google_location_dictionary["lng"]
    print "I am longitude", longitude



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
