import os
from typing import Optional, Union, Any
from nornir.core.deserializer.inventory import Inventory, HostsDict, GroupsDict
from base64 import b64encode
import simplejson as json
import urllib3
urllib3.disable_warnings()

import requests

class IPFInventory(Inventory):

    def __init__(
        self,
        ipf_url: Optional[str] = None,
        ipf_user: Optional[str] = None,
        ipf_password: Optional[str] = None,
        ipf_snapshot: Optional[str] = "$last",
        ssl_verify: Union[bool, str] = False,
        **kwargs: Any,
    ) -> None:

        """
        IP Fabric plugin
        API docs https://docs.ipfabric.io/api/
        Arguments:
            ipf_url: IP Fabric url, defaults to http://localhost:8080.
            ipf_user: username to access IP Fabric API
            ipf_password: password to access IP Fabric API
            ipf_snapshot: snapshot to read, details here https://docs.ipfabric.io/api/#tables
            ssl_verify: Enable/disable certificate validation or provide path to CA bundle file
        """

        ipf_url = ipf_url or os.environ.get("IPF_URL", "https://localhost")
        ipf_user = ipf_user or os.environ.get("IPF_USER", "admin")
        ipf_password = ipf_password or os.environ.get("IPF_PASSWORD", "admin")

        url = f"{ipf_url}/api/v1/tables/inventory/devices"

        credentials = b64encode(f"{ipf_user}:{ipf_password}".encode("utf-8")).decode(
            "utf-8"
        )
        headers = {
            "Content-type": "application/json",
            "Authorization": f"Basic {credentials}",
        }

        data = {
            "columns": [
                "sn",
                "hostname",
                "siteName",
                "loginIp",
                "loginType",
                "vendor",
                "platform",
                "family",
                "version",
            ],
            "filters": {},
            "snapshot": ipf_snapshot,
        }
        r = requests.post(
            url, data=json.dumps(data), headers=headers, verify=ssl_verify
        )

        if not r.status_code == 200:
            raise ValueError(f"Failed to get devices from IP Fabric {ipf_url}")

        ipf_devices = json.loads(r.content).get("data")

        hosts = {}
        groups = {}

        # map IPF family to netmiko platform names / netmiko device_type
        # list of IP Fabric supported device families https://docs.ipfabric.io/matrix/
        # list of netmiko supported device_types https://github.com/ktbyers/netmiko/blob/master/netmiko/ssh_dispatcher.py
        netmiko_platform_map = {
            "asa": "cisco_asa",
            "ios-xe": "cisco_xe",
            "ios-xr": "cisco_xr",
            "nx-os": "cisco_nxos",
            "wlc-air": "cisco_wlc",
            "pa-vm": "paloalto",
        }

        # napalm platform mapping https://napalm.readthedocs.io/en/latest/support/
        napalm_platform_map = {
            "nx-os": "nxos_ssh",
            "ios-xe": "ios",
            "ios-rx": "iosxr",
        }

        for d in ipf_devices:
            host: HostsDict = {"data": {}}
            group: GroupsDict = {"data": {}}

            # set groups from site, platform and vendor for filtering
            host["groups"] = [
                d.get("siteName"),
                d.get("platform"),
                d.get("family") or d.get("vendor"),
                d.get("vendor"),
            ]

            host["hostname"] = d.get("loginIp", "")

            # set netmiko platform
            host["platform"] = netmiko_platform_map.get(d["family"], d["family"])

            # set napalm platform
            host["connection_options"] = {
                "napalm": {
                    "platform": napalm_platform_map.get(d["family"], d["family"])
                }
            }

            host["data"]["family"] = d.get("family") or d.get("vendor")
            host["data"]["hostname"] = d.get("hostname")
            host["data"]["serial"] = d.get("sn")
            host["data"]["platform"] = d.get("platform")
            host["data"]["processor"] = d.get("processor")
            host["data"]["siteName"] = d.get("siteName")
            host["data"]["vendor"] = d.get("vendor")
            host["data"]["version"] = d.get("version")
            host["data"]["siteName"] = d.get("siteName")

            hosts[d.get("hostname") or d.get("id")] = host

            groups[d.get("siteName")] = {}
            groups[d.get("platform")] = {}
            groups[d.get("family") or d.get("vendor")] = {}
            groups[d.get("vendor")] = {}

        super().__init__(hosts=hosts, groups=groups, defaults={}, **kwargs)
