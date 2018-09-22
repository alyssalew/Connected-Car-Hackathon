# Makes a request to Lyft to get the oauth token
import requests
import json
import os

#Get Lyft secrets
LYFT_CLIENT_ID = os.environ['LYFT_CLIENT_ID']
LYFT_CLIENT_SECRET = os.environ['LYFT_CLIENT_SECRET']


def o_auth():
    headers = {
        "Content-Type": "application/json",
    }
    
    payload = {
        "grant_type": "client_credentials", 
        "scope": "public",
        LYFT_CLIENT_ID : LYFT_CLIENT_SECRET
    }

    r = requests.post("https://api.lyft.com/oauth/token", headers=headers, params=payload)
    print 'Status Code: {code}'.format(code=r.status_code)
    print r.json()

o_auth()