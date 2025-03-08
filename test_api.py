#!/usr/bin/env python3
''' test_api.py
    This script is used to test the API for the Conbee II'''

import json
import sys
import requests

port = '8080'
URL = 'http://192.168.1.44:'+ port
ESP32_MAC = '7c:2c:67:ff:fe:5d:3a:e8' # Note: Some endpoints require colons, some don't!
ESP_INSTALL_CODE = '83FED3407A939723A5C639B26916D505C3B5'

DECONZ_MAC = "00:21:2e:ff:ff:09:d2:20"

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
    # Check if the API key is already stored
    try:
        with open("apikey.txt", "r", encoding = "utf-8") as f:
            api_k = f.read()
            print("API Key: " + api_k)
            return api_k
    except FileNotFoundError:
        pass
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
            print(r_dict[0])
            # Save to file
            with open("apikey.txt", "w", encoding = "utf-8") as f:
                f.write(r_dict[0]['success']['username'])
            return r_dict[0]['success']['username']
    except requests.exceptions.RequestException as e:
        print(e.errno)
        print("Response: FAIL")
        return None

def send_permit_join(api_key_l: str, secs: int) -> None:
    '''
    Sends a 'permitjoin' command to open network
    '''
    payload = {"permitjoin": secs}
    api_str = URL + "/api/" + format(api_key_l) + "/config"
    print("Sending: " + api_str + ", payload = " + format(payload))
    try:
        response = requests.put(api_str, json=payload, timeout=10)
        if not response.ok:
            print("FAIL")
        else:
            print("Response: OK")
    except requests.exceptions.RequestException as e:
        print("Response: FAIL: " + e.errno)

def pair_with_install_code(api_key_l: str, mac_address: str, install_code: str) -> None:
    '''
    Pair with a device using an install code using the following format:

    PUT /api/<apikey>/devices/<device_mac_address>/installcode

    ref: https://dresden-elektronik.github.io/deconz-rest-doc/endpoints/devices/#pair-with-install-code

    Note: No colons in the mac_address!
    '''
    # Strip colons
    #mac_address = mac_address.replace(":", "")
    payload = {"installcode": install_code}
    api_str = URL + "/api/" + format(api_key_l) + "/devices/" + mac_address + "/installcode"
    print("Sending: " + api_str + ", payload = " + format(payload))
    try:
        response = requests.put(api_str, json=payload, timeout=10)
        if not response.ok:
            print("FAIL: " + response.text)
        else:
            print("Response: OK")
            return True
    except requests.exceptions.RequestException as e:
        print("Response: FAIL: " + e.errno)
        return False

def get_devices_list(api_key_l: str) -> None:
    '''
    Get a list of devices

    GET /api/<apikey>/devices

    ref: https://dresden-elektronik.github.io/deconz-rest-doc/endpoints/devices/#get-devices-list

    Note: Must have colons in the mac_address!
    '''
    api_str = URL + "/api/" + format(api_key_l) + "/devices"
    print("Sending: " + api_str)
    try:
        response = requests.get(api_str, timeout=10)
        if not response.ok:
            print("FAIL")
        else:
            print("Response: OK")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print("Response: FAIL: " + e.errno)

def get_device_details(api_key_l: str, mac_address: str) -> None:
    '''
    Get details of a device

    GET /api/<apikey>/devices/<device_mac_address>

    ref: https://dresden-elektronik.github.io/deconz-rest-doc/endpoints/devices/#get-device-details

    Note: Must have colons in the mac_address!
    '''
    api_str = URL + "/api/" + format(api_key_l) + "/devices/" + mac_address
    print("Sending: " + api_str)
    try:
        response = requests.get(api_str, timeout=10)
        if not response.ok:
            print("FAIL")
        else:
            print("Response: OK")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print("Response: FAIL: " + e.errno)

if __name__ == "__main__":
    #find_deconz()
    api_key = acquire_api_key()
    #send_permit_join(api_key, 60)
    get_devices_list(api_key)
    get_device_details(api_key, ESP32_MAC)
    pair_with_install_code(api_key, ESP32_MAC, ESP_INSTALL_CODE)
    sys.exit(0)
