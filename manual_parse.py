#!/usr/bin/python -tt
# Project: parsing_overview
# Filename: manual_parse
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "5/2/20"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

# This module is not part of Python and does need to be pip installed
import argparse
# Part of Python, no need to pip install this module
import re


def load_output():
    """
    this function just holds static semi formatted text from the show ip route command on an NX-os device
    :return: show_cmd_output
    """

    show_cmd_output = """
IP Route Table for VRF "default"
'*' denotes best ucast next-hop
'**' denotes best mcast next-hop
'[x/y]' denotes [preference/metric]
'%<string>' in via output denotes VRF <string>

10.98.98.0/24, ubest/mbest: 1/0, attached
    *via 10.98.98.1, Lo98, [0/0], 00:48:18, direct
10.98.98.1/32, ubest/mbest: 1/0, attached
    *via 10.98.98.1, Lo98, [0/0], 00:48:18, local
10.99.99.0/24, ubest/mbest: 1/0, attached
    *via 10.99.99.1, Lo99, [0/0], 00:48:18, direct
10.99.99.1/32, ubest/mbest: 1/0, attached
    *via 10.99.99.1, Lo99, [0/0], 00:48:18, local
172.16.0.1/32, ubest/mbest: 2/0, attached
    *via 172.16.0.1, Lo1, [0/0], 00:48:18, local
    *via 172.16.0.1, Lo1, [0/0], 00:48:18, direct
    """
    return show_cmd_output


def load_output_from_file(outfile = 'sample_output_nxos_shiproute.txt'):
    """
    Sample function that reads in a file of show command text and returns it
    The file is read using the readlines() method so data is actually a Python list and each element
    represents a line in the file.
    :param outfile:
    :return: data is a list of lines in the file
    """

    try:
        with open(outfile) as file:
            data = file.readlines()
        return data
    except Exception as e:
        print(f"ERROR! Cannot open file! \nAborting Script Execution")
        print(e)
        exit()


def main():

    # Load the semi formatted show command output and save into the data variable (string)
    # I put this in a function just to get it out of the way.  It also sets up the main part of the script to work
    # modularly so that at a later time you can write a function that goes out to the device and gets the output
    # One step at a time for now...
    data_as_string = load_output()

    # Process the text output of the show command and turn into a list of lines
    data_as_list = data_as_string.splitlines()

    # Example of loading the data from a file.
    # Because the load_output_from_file function loads the data using readlines() we can skip the string step and
    # go right to data_as_list and skip the above
    # data_as_list = load_output_from_file()

    # Initialize an empty list of mac lines which will contain lists of each line with a mac address
    # This will be a list of lists
    structured_data_list = []

    # Iterate over the lines and look for the mac address result line pattern
    # In a more production ready script this section would be replaced with a call to TextFMS if you were dealing
    # with saved show commands.
    # If a more sophisticated method was used to query the device (napalm, netmiko with TextFMS, pyATS and Genie) then
    # you would likely have saved that output in JSON or Pickle so that it could be loaded directly here as a
    # usable object
    # Example line:

    for line in data_as_list:
        # print(line)
        # mac_match = re.search(r'([0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})', line, re.IGNORECASE)
        # Use the re module search method to find each line in the text that matches the regular expression
        # which looks for a string which starts with 1 to 3 characters, one or more spaces, one to 4 digits, etc.
        # ^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$
        # https://riptutorial.com/regex/example/14146/match-an-ip-address
        regexp= r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}\/\d{1,2}'
        line_match = re.search(regexp, line, re.IGNORECASE)
        if line_match:
            # If the re search finds a match, split the line into a list (split on spaces)
            line_split = line_match.group().split()
            # append the line_split list to the mac_list (list of lists)
            structured_data_list.append(line_split)

    print(f"\nOutput data has been parsed into the variable structured_data_list of type {type(structured_data_list)}:"
          f"\nmac_list =\n{structured_data_list}")


    # 1. Calculate the total number of routes in the (default) routing table
    # 2. Determine if there is a default route
    # 3. Determine if a specific route is in the routing table
    print(f"\n===============  Answers to Questions ===============")
    print(f"\n\t1. Total Number of Routes: \t{len(structured_data_list)}:")
    # Now we have to iterate through our structured data in order to answer our questions
    # Assume there is no default route and that the specific route is not in the routing table
    default_rout_exists = "No"
    specific_route_exists = "No"
    for line in structured_data_list:
        if '0.0.0.0' in line[0]:
            default_rout_exists = "Yes"
        if arguments.prefix in line[0]:
            specific_route_exists = "Yes"
    print(f"\n\t2. Is there a default route?: \t{default_rout_exists}")
    print(f"\n\t3. Is {arguments.prefix} in the routing table: \t{specific_route_exists}\n")

# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python manual_parse' ")
    parser.add_argument('-p', '--prefix', help='Look for this prefix in the routing table Default: 10.99.99.1/32', action='store',
                        default='10.99.99.1/32')
    arguments = parser.parse_args()
    main()
