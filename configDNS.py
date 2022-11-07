'''Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
'''



import requests
import os, json
from dotenv import load_dotenv


load_dotenv()
api_key= os.environ["MERAKI_API_KEY"]

def get_orgs_and_networks():
    url = "https://api.meraki.com/api/v1/organizations"

    payload = None

    headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": api_key
    }

    orgs = requests.request('GET', url, headers=headers, data = payload).json()
    result=[]
    
    for org in orgs:
        
            org_entry = {
                "orgaid" : org['id'],
                "organame" : org['name'],
                "networks" : []
            }
            orgId=org['id']


            url = "https://api.meraki.com/api/v1/organizations/"+orgId+"/networks"

            payload = None

            headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Cisco-Meraki-API-Key": api_key
                }

            networks = requests.request('GET', url, headers=headers, data = payload).json()
            for network in networks:
                org_entry['networks'] += [{
                'networkid' : network['id'],
                'networkname' : network['name']
            }]
            result += [org_entry]

    return result


def getSerial(network_id):
    url = "https://api.meraki.com/api/v1/networks/" + network_id + "/devices"
    payload = None
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key":api_key
    }

    devices = requests.get(url, headers=headers, data = payload).json()
    serials=[]
    for device in devices:
        if device['model'].startswith('MR'):
            ap_entry={
                "serial": device['serial'],
                "name": device['name']
            }
            serials+=[ap_entry]
    return serials

def configDNS(dns,network_id):
    dns=dns
    global names
    names=[]
    
    serials=getSerial(network_id)
    for s in serials:

            url = "https://api.meraki.com/api/v1/devices/"+ s['serial'] +"/managementInterface"

            payload = None

            headers = {
         "Content-Type": "application/json",
            "Accept": "application/json",
         "X-Cisco-Meraki-API-Key": api_key
        }

            response = requests.request('GET', url, headers=headers, data = payload).json()
            if response['wan1']['usingStaticIp']== True:

                dns1=response['wan1']['staticDns'][0]
                payload ={
                "wan1": {
                    "staticDns": [dns1,dns]
                    }
                }

                response = requests.request('PUT', url, headers=headers, data = json.dumps(payload))
                
                if response.status_code!=200:
                    return False
                else:
                    names.append(s['name'])
    
    return True


