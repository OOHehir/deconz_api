#!/usr/bin/env python3
''' test_api.py
    This script is used to test the API for the Conbee II'''

import json
import sys
import requests

port = '8080'
URL = 'http://172.17.0.1:'+ port
USERNAME = '95F433C2B8'
ESP32_MAC = '7c:2c:67:5d:3a:e8'
ESP_INSTALL_CODE = '83FED3407A939723A5C639B26916D505C3B5'

def find_deconz() -> str | None:
    '''
    Find the IP address
    '''
    api_str = "http://phoson.de/discover"
    print("Sending: " + api_str)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try:
        response = requests.get(api_str, headers=headers, timeout=10)
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
        response = requests.post(api_str, json=payload, timeout=10)
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
        response = requests.put(api_str, json=payload, timeout=10)
        if not response.ok:
            print("FAIL")
        else:
            print("Response: OK")
    except requests.exceptions.RequestException as e:
        print("Response: FAIL: " + e.errno)

def pair_with_install_code(mac_address: str, install_code: str) -> None:
    '''
    Pair with a device using an install code using the following format:

    PUT /api/<apikey>/devices/<device_mac_address>/installcode
    '''
    payload = {"installcode": install_code}
    api_str = URL + "/api/" + USERNAME + "/devices/" + mac_address
    print("Sending: " + api_str + " payload = " + format(payload))
    try:
        response = requests.put(api_str, json=payload, timeout=10)
        if not response.ok:
            print("FAIL")
        else:
            print("Response: OK")
    except requests.exceptions.RequestException as e:
        print("Response: FAIL: " + e.errno)

if __name__ == "__main__":
   #find_deconz()
   #acquire_api_key()
   # send_permit_join(60)
   pair_with_install_code("7c:2c:67:5d:3a:e8", "83FED3407A939723A5C639B26916D505C3B5")
   sys.exit(0)
