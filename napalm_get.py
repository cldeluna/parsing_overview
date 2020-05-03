#!/usr/bin/python -tt
# Project: parsing_overview
# Filename: napalm_parse
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "5/1/20"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse
import napalm
import json


def get_dev_response(**devdets):
    """
    Function to connect to a device, execute command, and return response
    :param devdets: keyword argument - dictionary with device details for login
    :return: response
    """

    driver = napalm.get_network_driver(devdets['driver'])

    device = driver(hostname=devdets['hostname'], username=devdets['username'],
                    password=devdets['password'], optional_args={'port': devdets['port']})

    print(f"\n============ Connecting to device {devdets['hostname']}")
    device.open()

    # Get Napalm Facts
    print(f"\n==Object get_facts(): \n{json.dumps(device.get_facts(), indent=4)}")

    res = device.cli(devdets['commands'])
    print(f"\n==FULL RESPONSE: \n{res}")

    print(f"\n==Object is of type {type(res)} with keys {res.keys()}")
    print(json.dumps(res, indent=4, sort_keys=True))

    print(f"\n==Raw Output Command Response: \n{res['show ip route']}")
    return res


def main():
    """
    Simple script to grab the output of a show command using Napalm
    :return:
    """

    # pip install napalm
    # https://napalm.readthedocs.io/en/latest/installation/index.html#full-installation
    # #ios-xe-mgmt.cisco.com ansible_host=ios-xe-mgmt.cisco.com port=8181 username=root password=D_Vay!_10&

    # Testbed Devices - DevNet Always On Sandbox IOS-XE CSR1K and NX-OS
    device_login_info = [
        {
            'hostname': 'ios-xe-mgmt.cisco.com',
            'username': 'root',
            'password': 'D_Vay!_10&',
            'driver': 'ios',
            'port': 8181,
            'commands': ['show ip route']
        },
        {
            'hostname': 'sbx-nxos-mgmt.cisco.com',
            'username': 'admin',
            'password': 'Admin_1234!',
            'driver': 'nx-os',
            'port': 8181,
            'commands': ['show ip route']
        }
    ]

    # Save device information to a JSON file
    with open('network_devices.json', 'w') as outfile:
        json.dump(device_login_info, outfile, indent=4)

    # Get a response from the ios-xe device (first device)
    response = get_dev_response(**device_login_info[0])
    # print(f"\n\n{response}")
    return response

# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python napalm_get.py' ")
    arguments = parser.parse_args()
    main()
