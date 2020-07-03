'''

AUTOMATION DEMO

Demo script:
- get list of hosts from IPF using Nornir and a custom inventory plugins
- get NTP configuration of devices in a site using IPF API
- fix wrong NTP configurations using Nornir

Requirements:
- ipfapi (https://github.com/ipfabric/ipfapi)
- setup as described in README.md

Get IP Fabric API

    wget https://raw.githubusercontent.com/ipfabric/ipfapi/master/ipfapi.py

'''

# CODE

## Authenticate and get devices missing NTP configuration (no NTP sources)

from ipfapi import tokenRequest, getData
import os

server = os.environ.get("IPF_URL", "https://localhost")
username = os.environ.get("IPF_USER", "admin")
password  = os.environ.get("IPF_PASSWORD", "admin")
authData = { 'username': username, 'password' : password }
snapshotId = '$last'
devicesEndpoint = server + 'api/v1/tables/management/ntp/summary/'

devicesPayload = {
  'columns':["id","sn","hostname","siteKey","siteName","confSources","reachableSources","sources"],
  'filters':{"confSources":["eq",0],"siteName":["like","L38"]},
  'pagination':{"limit":100,"start":0},
  'snapshot':snapshotId,
  'sort':{"order":"asc","column":"sources"},
  'reports':"/technology/management/ntp/summary"
}

tokens = tokenRequest(f"{server}/", authData).json()
headers = { 'Authorization' : 'Bearer ' + tokens['accessToken'], 'Content-Type': 'application/json'}
apiEndpoint = server+'/api'+'/v1/tables/management/ntp/summary/'

# Get NTP data

data = getData(apiEndpoint, headers, devicesPayload).json().get('data')

# Show devices missing NTP sources

data

# Merge IP Fabric data to Nornir Inventory
'''
Note: Nornir inventory was created in demo1 from IP Fabric Inventory.
'''

for d in data:
    nr.inventory.hosts[d.get('hostname')]['ntpSources']=d.get('confSources')

# Verify NTP is now an attribute of the host

nr.inventory.hosts[data[0].get('hostname')].items()

# Notice ntpSources is zero

nr.inventory.hosts[data[0].get('hostname')].get('ntpSources')

# Use Nornir filter to find hosts missing ntpSources

noNTP = nr.filter(ntpSources=0)

noNTP.inventory.hosts

# Fix devices missing NTP Sources
'''
Set username and password to connect to devices
'''

nr.inventory.defaults.username = 'myusername'
nr.inventory.defaults.password = 'mypassword' 

'''
Fix NTP configuration
'''

from nornir.plugins.tasks.networking import netmiko_send_config
commands=['ntp server 10.0.10.10']
results =noNTP.run(task=netmiko_send_config,config_commands=commands)

'''
Now connect to the device and verify NTP configuration is fixed
'''

'''
BONUS: refresh host data from IP Fabric and run again this demo, notice the list of hosts with missing sources is empty now.
'''
