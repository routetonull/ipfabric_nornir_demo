# ipfabric_nornir_demo
inventory module for nornir and tutorials

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
