# Makes a request to Lyft to get the oauth token
import requests
import json
import os

#Get Lyft secrets
LYFT_CLIENT_ID = os.environ['LYFT_CLIENT_ID']
LYFT_CLIENT_SECRET = os.environ['LYFT_CLIENT_SECRET']


def o_auth():
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "grant_type": "client_credentials", 
        "scope": "public",
        LYFT_CLIENT_ID : LYFT_CLIENT_SECRET
    }

    r = requests.post("https://api.lyft.com/oauth/token", headers=headers, params=payload)
    print r
    print 'Status Code: {code}'.format(code=r.status_code)
    print r.json()

# o_auth()

def o_auth2():

    payload = {
        "client_id": LYFT_CLIENT_ID,
        "scope": "public%20profile%20rides.read%20rides.request",
        "state":"hello",
        "response_type":"code"
    }

    r = requests.get("https://www.lyft.com/oauth/authorize_app", params=payload)
    print 'Status Code: {code}'.format(code=r.status_code)

