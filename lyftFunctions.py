# Makes a request to Lyft to get the oauth token
import requests
import json
import os

#Get Lyft secrets
LYFT_CLIENT_ID = os.environ['LYFT_CLIENT_ID']
LYFT_CLIENT_SECRET = os.environ['LYFT_CLIENT_SECRET']

def get_ride_details(auth_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(auth_token)
    }

    r = requests.get("https://api.lyft.com/v1/rides/1180785462635055188", headers=headers)
    print 'Status Code: {code}'.format(code=r.status_code)

    response_dict = r.json()
    #driver_info = (response_dict['driver'], response_dict['vehicle'])
    print response_dict