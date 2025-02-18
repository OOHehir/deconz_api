#!/usr/bin/env python3


import requests
import sys
import json
from time import sleep
from datetime import datetime, timedelta

port = '8080'
URL = 'http://172.17.0.1:'+ port
USERNAME = '95F433C2B8'

def find_deconz() -> str | None:
    '''
    Find the IP address
    '''
    api_str = "http://phoson.de/discover"
    print("Sending: " + api_str)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try:
        response = requests.get(api_str, headers=headers)
        if not response.ok:
            print("FAIL")
            print(response.text)    #<- No useful information
            print(response.status_code)
            return None
        else:
            print("Response: OK")
            return response.text
    except requests.exceptions.RequestException as e:
        print(e.errno)
        print("Response: FAIL")
        return None

def acquire_api_key() -> str | None:
    '''
    Acquire an API key to interact with the Conbee II
    '''
    payload = {"devicetype": "my_application"}
    api_str = URL + "/api/"
    print("Sending: " + api_str + " payload = " + format(payload))
    try:
        response = requests.post(api_str, json=payload)
        if not response.ok:
            print("FAIL")
            print(response.text)    #<- No useful information
            print(response.status_code)
            return None
        else:
            print("Response: OK")
            print(response.text)
            r_dict = json.loads(response.text)
            print(type(r_dict))
            print(r_dict[0])
            return response.text
    except requests.exceptions.RequestException as e:
        print(e.errno)
        print("Response: FAIL")
        return None

def send_permit_join(secs: int) -> None:
    '''
    Sends a 'permitjoin' command to open network
    '''
    payload = {"permitjoin": secs}
    api_str = URL + "/api/" + USERNAME + "/config"
    print("Sending: " + api_str + " payload = " + format(payload))
    try:
        response = requests.put(api_str, json=payload)
        if not response.ok:
            print("FAIL")
        else:
            print("Response: OK")
    except requests.exceptions.RequestException as e:
        print("Response: FAIL")

if __name__ == "__main__":
   # find_deconz()
   # acquire_api_key()
   send_permit_join(60)
   sys.exit()