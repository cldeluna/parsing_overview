#!/usr/bin/python -tt
# Project: Dropbox (Indigo Wire Networks)
# Filename: textfsm.py
# claudia
# PyCharm

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "2019-04-12"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse
import textfsm
import csv
import json


def main():

    # Open the template file, and initialise a new TextFSM object with it.
    with open(arguments.template_file) as template_file_fh:
        fsm = textfsm.TextFSM(template_file_fh)

    # Read stdin until EOF, then pass this to the FSM for parsing.
    with open(arguments.output_file) as data_fh:
        input_data = data_fh.read()

    fsm_results = fsm.ParseText(input_data)

    if arguments.verbose:
        print("\nTextFSM Template Methods:")
        print(dir(fsm))
        print(f"\nFSM Values: \n\t{fsm.values}")
        print(f"\nFSM States: \n\t{fsm.states.keys()}")
        print(f"\nFSM States Full: \n\t{fsm.states}")
        print(f"\nFSM Value MAP:")
        for k,v in fsm.value_map.items():
            print(f"\tKey: {k} \tValue: {v}")

        print(f"\nTextFSM results variable is of type {type(fsm_results)} and has standard list Methods:")
        print(dir(fsm_results))

    print(f'\n\nTextFSM Results Header:\n{fsm.header}')
    print("="*40)
    for row in fsm_results:
        print(f"{row}")
    print("="*40)
    print("\n")

    # 1. Calculate the total number of routes in the (default) routing table
    # 2. Determine if there is a default route
    # 3. Determine if a specific route is in the routing table
    # Parsing Bonus Questions
    # 4. "What is the ip of the next hop for this route?"
    # 5. "What is the next hop interface?".
    print(f"\n===============  Answers to Questions ===============")
    print(f"\n\t1. Total Number of Routes: \t{len(fsm_results)}:")
    # Now we have to iterate through our structured data in order to answer our questions
    # Assume there is no default route and that the specific route is not in the routing table
    default_rout_exists = "No"
    specific_route_exists = False
    specific_route_text = "No"
    for line in fsm_results:
        if '0.0.0.0' in line[3]:
            default_rout_exists = "Yes"
        if arguments.prefix in line[3]:
            specific_route_exists = True
            specific_route_text = "Yes"
            next_hop_ip = line[7]
            next_hop_intf = line[8]

    print(f"\n\t2. Is there a default route?: \t{default_rout_exists}")
    print(f"\n\t3. Is {arguments.prefix} in the routing table: \t{specific_route_text}\n")
    print(f"\n==== Bonus Questions ====")

    if specific_route_exists:
        print(f"\n\t4. Next Hop IP for prefix {arguments.prefix} is: \t{next_hop_ip}")
        print(f"\n\t4. Next Hop Interface for prefix {arguments.prefix} is: \t{next_hop_intf}\n")

    if arguments.save:
    # Save to Text
        with open('output.txt', 'w') as out_fh:
            out_fh.write(f"{fsm.header}\n")
            [out_fh.write(f"{line}\n") for line in fsm_results]

        # Save to JSON
        # Create a list of dictionaries to save as JSON from the results data
        # Creating a list of dictionaries lets us iterate over the object and look for specific items
        # by name making the code more readable
        results_list_of_dicts = []
        for fsm_line in fsm_results:
            results_list_of_dicts.append({key:value for key, value in zip(fsm.header, fsm_line)})
        with open('output.json', 'w') as out_fh:
            json.dump(results_list_of_dicts, out_fh, indent=4)

        # Save to CSV
        # Insert the header row as the first element (0) in the list
        fsm_results.insert(0, fsm.header)
        with open('output.csv', 'w') as out_fh:
            csv_fh = csv.writer(out_fh)
            csv_fh.writerows(fsm_results)


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This script applys a textfsm template to a text file of unstructured "
                                                 "data (often show commands).  The resulting structured data is saved "
                                                 "as text (output.txt) and CSV (output.csv).",
                                     epilog="Usage: ' python textfsm.py <-t for optional template file> "
                                            "<-o for optional show output file>' ")

    parser.add_argument('-t', '--template_file',
                        help='TextFSM Template File Defaults to cisco_nxos_show_ip_route.textfsm',
                        action='store',
                        default='ntc-templates/templates/cisco_nxos_show_ip_route.textfsm')
    parser.add_argument('-o', '--output_file',
                        help='Show Command Output File Defaults to sample_output_nxos_shiproute.txt',
                        action='store',
                        default='sample_output_nxos_shiproute.txt')
    parser.add_argument('-p', '--prefix',
                        help='Look for this prefix in the routing table Default: 10.99.99.1',
                        action='store',
                        default='10.99.99.1')
    parser.add_argument('-s', '--save',
                        help='Save the results as Text, CSV, and JSON ',
                        action='store_true',
                        default=False)
    parser.add_argument('-v', '--verbose',
                        help='Enable all of the extra print statements used to investigate the results ',
                        action='store_true',
                        default=False)


    arguments = parser.parse_args()

    main()
