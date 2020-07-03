# IP FABRIC NORNIR DEMO

A plugin for nornir to collect the inventory from IP Fabric.

Requires an IP Fabric appliance with some devices in the inventory.

More information about IP Fabric: [https://ipfabric.io/](https://ipfabric.io/)

For more examples and code the discussion in [https://networktocode.slack.com/](https://networktocode.slack.com/) in the IP FABRIC channel.

## SETUP

Install nornir

    pip3 install nornir

Copy ipfabric.py to nornir inventory path (modify based on the Python version running on your machine)

    cp ipfabric.py /usr/local/lib/python3.6/dist-packages/nornir/plugins/inventory/

Edit ipf.env with the credentials to access IP Fabric API

    export IPF_URL=https://lab.ipfabric.io
    export IPF_USER=admin
    export IPF_PASSWORD=admin

Import the env file

    source ipf.env

Verify env vars are set

    env | grep IPF
