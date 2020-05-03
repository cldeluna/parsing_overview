#!/usr/bin/python -tt
# Project: parsing_overview
# Filename: netmiko_get
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "5/1/20"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse
import netmiko


def load_device_info(json_file='network_devices.json'):
    with open(json_file) as json_file:
        data = json.load(json_file)


def main():

    # Reminder
    # export NET_TEXTFSM='/Users/claudia/Dropbox (Indigo Wire Networks)/scripts/python/2020/parsing_overview/ntc-templates/templates/'

    # user = os.environ.get('username')
    # pwd = os.environ.get('password')
    # sec = os.environ.get('secret')


    # sbx-nxos-mgmt.cisco.com ansible_host=sbx-nxos-mgmt.cisco.com ansible_port=8181 username=admin password=Admin_1234!
    # ios-xe-mgmt.cisco.com ansible_host=ios-xe-mgmt.cisco.com port=8181 username=root password=D_Vay!_10&

    dev = {
        'device_type': 'cisco_nxos',
        'ip' : 'sbx-nxos-mgmt.cisco.com',
        'username' : 'admin',
        'password' : 'Admin_1234!',
        'secret' : 'Admin_1234!',
        'port' : 8181

    }

    # RAW Parsing with Python
    if arguments.netmiko_only or arguments.all:
        print(f"\n===============  Netmiko ONLY ===============")
        try:
            dev_conn = netmiko.ConnectHandler(**dev)
            dev_conn.enable()
            response = dev_conn.send_command('show ip route')
            print(f"\nResponse is of type {type(response)}\n")
            print(response)
            # because the response is a string we need to do some string manipulation
            # first we need to split the string into lines
            resp = response.splitlines()
            # now we should have a list in rest over which we can iterate
            print(f"\nSplit Response is of type {type(resp)}\n")
            print(resp)
            find_string = "10.99.99.1/32"
            # look
            for line in resp:
                if find_string in line:
                    print(f"******** FOUND LINE! ******\n{line}\n")

        except Exception as e:
            print(e)

    if arguments.netmiko_textfsm or arguments.all:
        print(f"\n===============  Netmiko with TEXTFSM OPTION  ===============")
        try:
            dev_conn = netmiko.ConnectHandler(**dev)
            dev_conn.enable()
            response = dev_conn.send_command('show ip route', use_textfsm=True)
            print(f"\nResponse is of type {type(response)}\n")
            print(response)

            # 1. Calculate the total number of routes in the (default) routing table
            # 2. Determine if there is a default route
            # 3. Determine if a specific route is in the routing table
            # Parsing Bonus Questions
            # 4. "What is the ip of the next hop for this route?"
            # 5. "What is the next hop interface?".
            print(f"\n===============  Answers to Questions ===============")
            print(f"\n\t1. Total Number of Routes: \t{len(response)}:")
            # Now we have to iterate through our structured data in order to answer our questions
            # Assume there is no default route and that the specific route is not in the routing table
            default_rout_exists = "No"
            specific_route_exists = False
            specific_route_text = "No"
            for line in response:
                if '0.0.0.0' in line['network']:
                    default_rout_exists = "Yes"
                if arguments.prefix in line['network']:
                    specific_route_exists = True
                    specific_route_text = "Yes"
                    next_hop_ip = line['nexthop_ip']
                    next_hop_intf = line['nexthop_if']

            print(f"\n\t2. Is there a default route?: \t{default_rout_exists}")
            print(f"\n\t3. Is {arguments.prefix} in the routing table: \t{specific_route_text}\n")
            print(f"\n==== Bonus Questions ====")

            if specific_route_exists:
                print(f"\n\t4. Next Hop IP for prefix {arguments.prefix} is: \t{next_hop_ip}")
                print(f"\n\t4. Next Hop Interface for prefix {arguments.prefix} is: \t{next_hop_intf}\n")

        except Exception as e:
            print(e)

# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python netmiko_get.py -a ' ")

    parser.add_argument('-a', '--all',
                        help='Execute all the Netmiko sections of the script',
                        action='store_true',
                        default=False)
    parser.add_argument('-n', '--netmiko_only',
                        help='Execute the Netmiko Only section of the script',
                        action='store_true',
                        default=False)
    parser.add_argument('-t', '--netmiko_textfsm',
                        help='Execute the Netmiko with TextFSM section of the script',
                        action='store_true',
                        default=False)
    parser.add_argument('-p', '--prefix',
                        help='Look for this prefix in the routing table Default: 10.99.99.1/32',
                        action='store',
                        default='10.99.99.1')
    arguments = parser.parse_args()
    main()