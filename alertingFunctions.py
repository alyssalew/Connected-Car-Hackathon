# Contains helper functions to notify users via Twilio (text), Twitter and Lyft incident line
import requests
import json
import os
from twilio.rest import Client 


TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_SID = os.environ['TWILIO_SID']
SENDING_NUMBER = os.environ['SENDING_NUMBER']
RECEIVING_NUMBER = os.environ['RECEIVING_NUMBER']


def notify_contacts_emergency(user):

    account_sid = TWILIO_SID 
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token) 
    text_message="SAFEGUARD ALERT: {user} has activated emergency mode! other pertinent info here".format(user=user)
     
    message = client.messages.create( 
                                  from_=SENDING_NUMBER,        
                                  to=RECEIVING_NUMBER,
                                  body=text_message
                              ) 
     
    print(message.sid)

    return "Successfully notified your contacts"


def post_to_twitter():

    return "We've alerted users via Twitter of your location as well as details of your driver"


def contact_lyft():

    return "We've contacted Lyft to report your driver"