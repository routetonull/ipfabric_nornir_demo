Setup the environment as described on README.MD

## INVENTORY PLUGIN

Launch python3. 

Import inventory from IP Fabric

    from nornir import InitNornir
    nr = InitNornir(
        core={"num_workers": 10},
        inventory={
            "plugin":"nornir.plugins.inventory.ipfabric.IPFInventory",
            "options": {
                "ssl_verify": False,
            },
        },
        logging={
            "enabled": False,
        },
    )

Alternate method: provide url and credentials in code

    from nornir import InitNornir
    nr = InitNornir(
        core={"num_workers": 10},
        inventory={
            "plugin":"nornir.plugins.inventory.ipfabric.IPFInventory",
            "options": {
                "ipf_url":"https://lab.ipfabric.io",
                "ipf_user":"admin",
                "ipf_password":"admin",
                "ssl_verify": False,
            },
        },
        logging={
            "enabled": False,
        },
    )

## NORNIR INVENTORY BASICS

List all hosts imported by the plugin:

    nr.inventory.hosts

Count the hosts:

    len(nr.inventory.hosts)

Confirm the same number of hosts are on IP Fabric GUI.

Verify a single host:

    nr.inventory.hosts['L43AC29'].items()

## NORNIR INVENTORY FILTERING

Example of using Nornir filtering capabilities applied to attributes imported by IP Fabric like siteName and vendor.

Filter hosts of a particular site:

    site_L38 = nr.filter(siteName='L38')

List all hosts of the site

    site_L38.inventory.hosts

Count the hosts of the site

    len(site_L38.inventory.hosts)

Filter only PaloAlto firewalls of site HWLAB:

    HWLABpaloalto = nr.filter(siteName="HWLAB").filter(vendor="paloalto")
    HWLABpaloalto.inventory.hosts

Verify on IPFABRIC GUI applying the same filter, the devices in list should match.
