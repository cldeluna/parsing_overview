# Network Programability Parsing Solutions

For anyone starting or continuing in Network Programability and Automation, parsing is a key skill if you have to work with any kind of legacy equipment or equipment without any of the "modern conveniences" (aka APIs).

If you are relatively new, you may wonder why "parsing" is even relevant in Network Programability.

Pretty much everything we do as humans follows this pattern:

| Information | Cognition        | Action           |
| ----------- | ---------------- | ---------------- |
| Text data   | Network Engineer | Network Engineer |

I use those terms deliberately because of their human focus.

### Yesterday

In the networking of yesterday, the human is the nexus of Networking.

When we rely on human cognition, we know precisely what the information below means.  And we can answer a myriad of questions from this small snippet of information.  We know if the interface is access or trunk, what media, if its connected to something, how the connection negotiated, and the speed.

```
Port      Name               Status       Vlan       Duplex  Speed Type
Fa1/0/1                      connected    1          a-full  a-100 10/100BaseTX

```

### Today

In the networking of today, the fundamental shift is that the nexus is now Compute.  That isn't to say the human is not needed but rather that the human is not needed in the same places performing the same functions.   Today this shift results in a new pattern:

| Data            | Compute                                          | Execute                                                      |
| --------------- | ------------------------------------------------ | ------------------------------------------------------------ |
| Structured Data | Script, Program, Application, Computing Platform | Network Engineer (optional), Script, Program, Application, Computing Platform |

...and herein lies the problem.  

Where before we had our brains in the middle of **network configuration and operations** today we have the option of having compute there.   Compute, whether that is a process, an application, or a script, needs to deal with information differently.  Compute does not "understand" the way a human can.  Put differently the computer can't parse the information in the same way we can and so has to consume information differently.

When cognition turns into compute we have to package the information differently. 

### Why must we parse?

We find ourselves needing to parse data so that we can package that data in a way that is consumable by our compute.

A Human can take the information below and immediately answer the question. "What version of software is on this device?"

To Compute, the information is just a bunch of text (bits) and so for Compute to answer that same question we have to process or "parse" the information into a structure that compute can use.

So when dealing with devices that cannot return "structured data" we have to take the information that the device does return (a bunch of text) and manipulate it so that it can be used by Compute.  

We have to parse.

| Information                                                  | Data (Structured Data)                                       |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Cisco Nexus Operating System (NX-OS) Software<br/>TAC support: http://www.cisco.com/tac<br/>Documents: http://www.cisco.com/en/US/products/ps9372/tsd_products_support_series_home.html<br/>Copyright (c) 2002-2019, Cisco Systems, Inc. All rights reserved....<sniped for brevety><br/><br/>Nexus 9000v is a demo version of the Nexus Operating System<br/><br/>Software<br/>  BIOS: version <br/> <span style="color:red">NXOS: version 9.3(3)</span><br/>  BIOS compile time:  <br/>  NXOS image file is: bootflash:///nxos.9.3.3.bin<br/>  NXOS compile time:  12/22/2019 2:00:00 [12/22/2019 14:00:37]<br/><br/><br/>Hardware<br/>  cisco Nexus9000 C9300v Chassis <br/>  Intel(R) Xeon(R) Platinum 8176 CPU @ 2.10GHz with 16409068 kB of memory.<br/>  Processor Board ID 9N3KD63KWT0<br/><br/>  Device name: sbx-n9kv-ao<br/>  bootflash:    4287040 kB<br/>Kernel uptime is 0 day(s), 5 hour(s), 45 minute(s), 26 second(s)<br/><br/>Last reset <br/>  Reason: Unknown<br/>  System version: <br/>  Service: <br/><br/>plugin<br/>  Core Plugin, Ethernet Plugin<br/><br/>Active Package(s):<br/>        mtx-openconfig-all-1.0.0.0-9.3.3.lib32_n9000<br/>sbx-n9kv-ao# | {<br/>    "platform": {<br/>        "name": "Nexus",<br/>        "os": "NX-OS",<br/>        "software": {<br/>            <span style="color:red">"system_version": "9.3(3)"</span>,<br/>            "system_image_file": "bootflash:///nxos.9.3.3.bin",<br/>            "system_compile_time": "12/22/2019 2:00:00 [12/22/2019 14:00:37]"<br/>        },<br/>        "hardware": {<br/>            "model": "Nexus9000 C9300v",<br/>            "chassis": "Nexus9000 C9300v",<br/>            "slots": "None",<br/>            "rp": "None",<br/>            "cpu": "Intel(R) Xeon(R) Platinum 8176 CPU @ 2.10GHz",<br/>            "memory": "16409068 kB",<br/>            "processor_board_id": "9N3KD63KWT0",<br/>            "device_name": "sbx-n9kv-ao",<br/>            "bootflash": "4287040 kB"<br/>        },<br/>        "kernel_uptime": {<br/>            "days": 0,<br/>            "hours": 5,<br/>            "minutes": 45,<br/>            "seconds": 26<br/>        },<br/>        "reason": "Unknown"<br/>    }<br/>} |



## A Smorgasbord of Parsing Options

We are lucky we have many parsing options today.  

Anyone who has been at this a while can attest to the frustration of "do it yourself" parsing.  This generally takes the form of basic string manipulation in whatever language you were scripting in and regular expressions.   You finally got your regular expression to do what you needed and then the device manufacturer changed the format of the output so you were constantly fiddling to get the results you wanted.  

Make no mistake, that still happens, but there is a layer of abstraction now and a bevy of tools to make it easier.  Let's look at some of the more mainstream options and how we would use them to solve a particular problem.  

Use Case:

We would like to execute a "show ip route" command and: 

1. Calculate the total number of routes in the (default) routing table
2. Determine if there is a default route
3. Determine if a specific route is in the routing table

We start this by getting the data we need from the device (or devices) in question and then we analyze it to answer our three questions above.



#### Getting the data

First we have to determine how we are getting the data:

- Dynamically by logging into the device and parsing the real-time output
- Statically by processing resulting show command files

There are good reasons to be prepared for both.  If you are just starting out, you may be more comfortable working on static files of show command output rather than live devices.   I was.   Later on that served me well because there are times when I have to analyze a clients network and all they are comfortable sharing are scrubbed configs and show command results or their config backup repository.  This also served me well in testing, where, for example, I have to snapshot the state of a device and then validate against that snapshot.  

Eventually you want to do this real time and so you have to always consider how you want to execute this on live devices.  

The tools we will review here will be evaluated 

- Parsing dynamic real-time data
- Parsing static data
- Implementing logic
- Manipulating data



As we look at different options, some tools lend themselves better to one scenario over the other.

1. Manually Parsing the Output in Python
2. Python and CiscoConfParse
3. TextFSM
4. Python and Netmiko
5. Python and Napalm
6. Ansible 
7. Nornir
8. Python and pyATS 

Note:  Obviously static data can be obtained manually by logging in to the devices and saving the output either manually or via your SSH client.   This option is not a valid option in to

Legend:

- Device = one or more Network Devices
- Show Output = Semi formatted text output from Device
- Structured Data = Show command output text in a Python data structure which can be used natively in your Python script to get to the data you are interested in

| Data Options                 | Inputs (what you need to get started) | Outputs (what you get)                                       | Notes                                                        | When to Use                                                  |
| ---------------------------- | ------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Manual                       | You*<br />Device                      | Show Output                                                  | Please Stop this!                                            | Never!                                                       |
| Python and Parsing "by Hand" | Output                                | String Search                                                | You can get structured data but this is doing it the hard way.   <br />With Python and the built in string method and the re module (also part of Python) you can search for a pattern and write code to get data into a python data structure (list, dictionary, and nested combinations of both) | When you want to do something quick and dirty or when everything else fails.  It is good to understand how this works. |
| Python and CiscoConfParse    | Output                                | Structured Data                                              | This is probably the oldest (first commit in 2008 with lots of work in 2015 and still maintained) module in this list and I include it here for completeness.  This module parses configurations (no longer limited to Cisco). I mention it here because its handy to have this in your toolbox and in general some of the newer modules focus more on operational and state data rather than the configuration itself.  In some cases you want to look at the configuration.<br />[Mike Pennington's CiscoConfParse](https://github.com/mpenning/ciscoconfparse) | When you have to parse out nested sections of a configuration file. |
| Python and TextFSM           | Output                                | Structured Data                                              | With the NTC Template Library quite bit of the heavy lifting (parsing) has been done for you.  If there is no TextFMS template for your command or text, you can build your own!<br />[Network to Code TextFSM Parsing Templates repository](https://github.com/networktocode/ntc-templates) | This is a workhorse.  Great for parsing files.               |
| Python and Netmiko           | Device                                | Output                                                       | Here we use a Python script and Netmiko to connect to Devices and obtain Output (show command text output) | Great for parsing show commands directly from the device (vs a file) |
| Python, Netmiko, and TextFSM | Device                                | Structured Data                                              | Here we use a Python script and Netmiko to connect to Devices and we can take that output and process it through TextFSM in a separate step but why would we do this now that Netmiko can do that for us in a single statement with its [native TextFSM integration](https://pynet.twb-tech.com/blog/automation/netmiko-textfsm.html). |                                                              |
| Python and Napalm            | Device                                | Structured Data *for supported   getters*                    | Using a Python script and the Napalm module you are only limited by the Napalm getters that are available.   You can use Napalm to get the semi formatted text back and then process with something like TextFSM.<br /> | Great for multi vendor environments when you need the same structured data across output from different vendors |
| Ansible                      | Device                                | Structured Data *for supported modules or with integrations* | Using an Ansible Playbook and Ansible modules you can execute show commands against your Devices.  Parsing is a bit more limited here without extra work (your own filter, integrations, etc.) | Great when modules support your use case Great when Genie supports your use case (the command you need to parse or when you already get structured data back |
| Python and Nornir            | Device                                | Structured Data                                              | Using a Python script, you get the ease of using an Ansible like host file to hold all of your device information, with the flexibility of python.  Since Nornir leverages Netmiko heavily you also get TextFMS integration! |                                                              |
| Python and PyATS             | Device<br />and/or<br />Output        | Structured Data *for supported Parsers*                      | Using a Python script and pyATS (now bundled with the Genie library which contains, among other things, parsers for common show commands) you can, in a single command log in to your Devices and obtain Structured Data in one command much like the Netmiko-TextFMS integration<br />[Supported Parsers](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers) | Great when Genie supports your use case (the command you need to parse) |

\* *You are involved in all of these steps, obviously, but I call out "You" in the Manual process because it is so manual*



#### Manual 

<u>Sample script:</u>  None!!! 

We are familiar with this process of logging in to the device, executing commands, and saving them to a text file.   If you are still doing this, please stop!  

```
csr1000v-1(config)#no logging console
csr1000v-1(config)#line console 0
csr1000v-1(config-line)#exec-timeout 0
csr1000v-1(config-line)#end
csr1000v-1# show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, m - OMP
       n - NAT, Ni - NAT inside, No - NAT outside, Nd - NAT DIA
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       H - NHRP, G - NHRP registered, g - NHRP registration summary
       o - ODR, P - periodic downloaded static route, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is 10.10.20.254 to network 0.0.0.0

S*    0.0.0.0/0 [1/0] via 10.10.20.254, GigabitEthernet1
      1.0.0.0/32 is subnetted, 1 subnets
S        1.1.1.1 is directly connected, Null0
      10.0.0.0/8 is variably subnetted, 2 subnets, 2 masks
C        10.10.20.0/24 is directly connected, GigabitEthernet1
L        10.10.20.48/32 is directly connected, GigabitEthernet1
S     192.0.2.0/24 is directly connected, GigabitEthernet1
S     203.0.113.0/24 [1/0] via 10.10.20.254

```

Using this process you get Output that you typically then save to a text file the can be used at a later time.  This becomes the input to your script but there are much easier ways to get this input!



#### Python and Parsing "by Hand"

<u>Sample Script:</u>  ***manual\_parse.py***

We are going to cover manual parsing because this is foundational and you will never appreciate all the subsequent modules and frameworks until you do a little bit of this.

Lets take a small portion of output.

```
10.98.98.0/24, ubest/mbest: 1/0, attached
    *via 10.98.98.1, Lo98, [0/0], 00:10:55, direct
10.98.98.1/32, ubest/mbest: 1/0, attached
    *via 10.98.98.1, Lo98, [0/0], 00:10:55, local
```

Because we are asking pretty simple questions, this isn't too bad.  We can develop a regular expression to pick out the routes and call it a day.  However, consider what happens when we ask "What is the ip of the next hop for this route?" or "What is the next hop interface?".  Now we have to parse multi line content and keep the first line with the route and the second indented line together.  This gets more complicated.   

But for our simple example all we need to do is get the output data and manipulate it.

In the script we read it in from a variable (the script shows how to read it in from a file as well) split up the string into lines and then parse out the information we want and put that into a python list of lists.

[This link](https://regex101.com/r/oDIWbw/2) will explain what the regular expression below is looking for in each line.

```python
    # Load the semi formatted show command output and save into the data variable (string)
    # I put this in a function just to get it out of the way.  It also sets up the main part of the script to work
    # modularly so that at a later time you can write a function that goes out to the device and gets the output
    # One step at a time for now...
    data_as_string = load_output()

    # Process the text output of the show command and turn into a list of lines
    data_as_list = data_as_string.splitlines()

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
        regexp= r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}\/\d{1,2}'
        line_match = re.search(regexp, line, re.IGNORECASE)
        if line_match:
            # If the re search finds a match, split the line into a list (split on spaces)
            line_split = line_match.group().split()
            # append the line_split list to the mac_list (list of lists)
            structured_data_list.append(line_split)
```



Once we have that it is a simple matter of some some logic to get to our answers.

```python
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
```



And we have our answers:



```
(parsing) claudia@Claudias-iMac parsing_overview % python manual_parse.py

Output data has been parsed into the variable structured_data_list of type <class 'list'>:
mac_list =
[['10.98.98.0/24'], ['10.98.98.1/32'], ['10.99.99.0/24'], ['10.99.99.1/32'], ['172.16.0.1/32']]

===============  Answers to Questions ===============

        1. Total Number of Routes:      5:

        2. Is there a default route?:   No

        3. Is 10.99.99.1/32 in the routing table:       Yes

(parsing) claudia@Claudias-iMac parsing_overview % 

```



#### Python and CiscoConfParse

<u>Sample Script:</u>  None but check out the [Kirk Byers write up](https://pynet.twb-tech.com/blog/python/ciscoconfparse.html)

I won't spend too much time on CiscoConfParse, nor do I have an example,  but I do want to get it on your radar. You can read much more about it on [Mike Pennington's page](http://pennington.net/py/ciscoconfparse/intro.html).

It's fantastic for compliance (that was its original mission) and to that end, it is the perfect tool to use to dig into configurations that have a hierarchy that is "space" based.    For example, I have a script that looks for interfaces without dot1x configured and this is a great tool to use for things like that.



#### TextFSM

<u>Sample Script:</u>   ***textfsm\_parse.py***

TextFSM is a [Python module](https://github.com/google/textfsm) developed by Google for parsing "semi-formatted" text.  This means that the text has patterns that we can use to match against and extract information.   

If you have lots of legacy devices, perhaps devices that are older or not so main stream, I do urge you to get familiar with this module.  There are excellent resources out there and I list the ones I found most useful in this post *[A quick example of using TextFSM to parse data from Cisco show commands – Python3 Version](https://gratuitous-arp.net/a-quick-example-of-using-textfsm-to-parse-data-from-cisco-show-commands-python3-version/)*.

The TextFMS module can be used in your script directly or indirectly via another module or framework. For example Netmiko supports direct integration with TextFMS, so you can use its with Nornir,  and you can set up Ansible to use TextFMS.  All of these integrations use the Network to Code Template repository but you an also [build your own](https://gratuitous-arp.net/building-a-custom-textfsm-template/).

The accompanying script can take options for a TextFSM template, a text show command output file, run in verbose mode, and save the parsed results in a variety of formats.



```
(parsing) claudia@Claudias-iMac parsing_overview % python textfsm_parse.py -h
usage: textfsm_parse.py [-h] [-t TEMPLATE_FILE] [-o OUTPUT_FILE] [-s] [-v]

This script applys a textfsm template to a text file of unstructured data
(often show commands). The resulting structured data is saved as text
(output.txt) and CSV (output.csv).

optional arguments:
  -h, --help            show this help message and exit
  -t TEMPLATE_FILE, --template_file TEMPLATE_FILE
                        TextFSM Template File Defaults to
                        cisco_nxos_show_ip_route.textfsm
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Show Command Output File Defaults to
                        sample_output_nxos_shiproute.txt
  -s, --save            Save the results as Text, CSV, and JSON
  -v, --verbose         Enable all of the extra print statements used to
                        investigate the results

```

In its simplest form, without any arguments the script will parse the sample_output_nxos_shiproute.txt using the cisco_nxos_show_ip_route.textfsm Network to Code TextFSM template.

```
(parsing) claudia@Claudias-iMac parsing_overview % python textfsm_parse.py


TextFSM Results Header:
['VRF', 'PROTOCOL', 'TYPE', 'NETWORK', 'MASK', 'DISTANCE', 'METRIC', 'NEXTHOP_IP', 'NEXTHOP_IF', 'UPTIME', 'NEXTHOP_VRF', 'TAG', 'SEGID', 'TUNNELID', 'ENCAP']
========================================
['default', 'direct', '', '10.98.98.0', '24', '0', '0', '10.98.98.1', 'Lo98', '00:48:18', '', '', '', '', '']
['default', 'local', '', '10.98.98.1', '32', '0', '0', '10.98.98.1', 'Lo98', '00:48:18', '', '', '', '', '']
['default', 'direct', '', '10.99.99.0', '24', '0', '0', '10.99.99.1', 'Lo99', '00:48:18', '', '', '', '', '']
['default', 'local', '', '10.99.99.1', '32', '0', '0', '10.99.99.1', 'Lo99', '00:48:18', '', '', '', '', '']
['default', 'local', '', '172.16.0.1', '32', '0', '0', '172.16.0.1', 'Lo1', '00:48:18', '', '', '', '', '']
['default', 'direct', '', '172.16.0.1', '32', '0', '0', '172.16.0.1', 'Lo1', '00:48:18', '', '', '', '', '']
========================================

```



IMPORTANT:  Notice that with TextFSM we can now answer the additional questions.

"What is the ip of the next hop for this route?"

"What is the next hop interface?". 

The TextFSM parsing engine handles the multi line text and extracts the information we need to answer those questions.

The other thing to notice is that with TextFSM we pick up an additional route (6 vs 5). That is because with TextFMS we get a record or entry for each prefix **and path**.

The final entry for 172.16.0.1/32 has two entries in the routing table.

Script Output:

```

===============  Answers to Questions ===============

        1. Total Number of Routes:      6:

        2. Is there a default route?:   No

        3. Is 10.99.99.1 in the routing table:  Yes


==== Bonus Questions ====

        4. Next Hope IP for prefix 10.99.99.1 is:       10.99.99.1

        4. Next Hope Interface for prefix 10.99.99.1 is:        Lo99

(parsing) claudia@Claudias-iMac parsing_overview % 

```



#### Python and Netmiko

<u>Sample Script:</u>  ***netmiko_get.py - n*** 

The [Netmiko module](https://pypi.org/project/netmiko/) is the definitive module to use to connect to your network devices.  Netmiko is mature and feature rich and supports a wide variety of vendors.   This is a [must learn](https://pynet.twb-tech.com/class-pyauto.html).

Netmiko can be used to connect to your Devices and grab the show command output which you can then "parse" either manually or with TextFMS.

Run the netmiko_get.py script with the -n argument to run the Netmiko only section.  Here we get back our text response which is a Python string and which can then be used with TextFSM manually or which can be used in manual parsing.  In this this example we don't parse as much as search for the prefix 10.99.99.1/32 with just the Python string feature "in".

```python
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
```



Output of the script is:

```
(parsing) claudia@Claudias-iMac parsing_overview % python netmiko_get.py -n

===============  Netmiko ONLY ===============

Response is of type <class 'str'>

IP Route Table for VRF "default"
'*' denotes best ucast next-hop
'**' denotes best mcast next-hop
'[x/y]' denotes [preference/metric]
'%<string>' in via output denotes VRF <string>

10.98.98.0/24, ubest/mbest: 1/0, attached
    *via 10.98.98.1, Lo98, [0/0], 05:15:51, direct
10.98.98.1/32, ubest/mbest: 1/0, attached
    *via 10.98.98.1, Lo98, [0/0], 05:15:51, local
10.99.99.0/24, ubest/mbest: 1/0, attached
    *via 10.99.99.1, Lo99, [0/0], 05:15:51, direct
10.99.99.1/32, ubest/mbest: 1/0, attached
    *via 10.99.99.1, Lo99, [0/0], 05:15:51, local
172.16.0.1/32, ubest/mbest: 2/0, attached
    *via 172.16.0.1, Lo1, [0/0], 05:15:51, local
    *via 172.16.0.1, Lo1, [0/0], 05:15:51, direct

Split Response is of type <class 'list'>

['IP Route Table for VRF "default"', "'*' denotes best ucast next-hop", "'**' denotes best mcast next-hop", "'[x/y]' denotes [preference/metric]", "'%<string>' in via output denotes VRF <string>", '', '10.98.98.0/24, ubest/mbest: 1/0, attached', '    *via 10.98.98.1, Lo98, [0/0], 05:15:51, direct', '10.98.98.1/32, ubest/mbest: 1/0, attached', '    *via 10.98.98.1, Lo98, [0/0], 05:15:51, local', '10.99.99.0/24, ubest/mbest: 1/0, attached', '    *via 10.99.99.1, Lo99, [0/0], 05:15:51, direct', '10.99.99.1/32, ubest/mbest: 1/0, attached', '    *via 10.99.99.1, Lo99, [0/0], 05:15:51, local', '172.16.0.1/32, ubest/mbest: 2/0, attached', '    *via 172.16.0.1, Lo1, [0/0], 05:15:51, local', '    *via 172.16.0.1, Lo1, [0/0], 05:15:51, direct', '']
******** FOUND LINE! ******
10.99.99.1/32, ubest/mbest: 1/0, attached

```



<u>Sample Script:</u>   ***textfsm\_parse.py - t***

However, as of [Netmiko 2.0](https://pynet.twb-tech.com/blog/automation/netmiko-textfsm.html), TextFSM parsing is integrated!  This means that you can now connect to a device, execute a command, and parse the result with the TextFSM Network to Code templates in a single command!

Note the **use_textfsm=True** option:

```
response = dev_conn.send_command('show version', use_textfsm=True)
```





#### Python and Napalm

<u>Sample Script:</u>  

[Napalm](https://napalm.readthedocs.io/en/latest/) (Network Automation and Programmability Abstraction Layer with Multivendor support) is a Python module designed to interact with live network devices and return structured data.  Napalms sweet spot is in a multi-vendor environment because it not only returns structured data from your show commands but it returns the SAME structure across various vendors.    

Think of the power this efforts if you are supporting a multi vendor environment and you need to check for a particular vlan on all your switches be they Arista, Cisco Catalyst, Cisco Nexus, or Juniper.   You can use the same code in your logic across all of those devices!

Napalm supports specific devices and specific "getters" which will "get" specific information from your device and return in as structured data.

For our example, 'show ip route' has no [supported "getter"](https://napalm.readthedocs.io/en/latest/support/index.html) so we get back a bit of structured data but the command output itself is not parsed.

We get back a dictionary with one key ['show ip route'] which has our show command output as a string, which we now have to parse.

```
Object is of type <class 'dict'> with keys dict_keys(['show ip route'])
{
    "show ip route": "Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP\n       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area \n       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2\n       E1 - OSPF external type 1, E2 - OSPF external type 2\n       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2\n       ia - IS-IS inter area, * - candidate default, U - per-user static route\n       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP\n       a - application route\n       + - replicated route, % - next hop override, p - overrides from PfR\n\nGateway of last resort is 10.10.20.254 to network 0.0.0.0\n\nS*    0.0.0.0/0 [1/0] via 10.10.20.254, GigabitEthernet1\n      10.0.0.0/8 is variably subnetted, 2 subnets, 2 masks\nC        10.10.20.0/24 is directly connected, GigabitEthernet1\nL        10.10.20.48/32 is directly connected, GigabitEthernet1"
}

```





##### Recommended Reading

[Fighting CLI cowboys with Napalm - An Introduction](https://networklore.com/napalm-introduction/)



#### Ansible

Ansible has a plethora of networking modules which can make your job a breeze, particularly if you are trying to validate a configuration item, generate a configuration, or execute commands and save the output (without parsing).

My "go to" network reconnaissance scripts, when I do have access to a clients network, are in Ansible.

For the activities Ansible supports (a module exists), it is **mindnumpingly easy** and I leverage Ansible wherever I can.  Outside of that, it can be complicated depending on your skill set.  For me, if I need to apply lots of logic or manipulate the data, I find it is easier to work in Python and some of the other modules we have in our toolbox (Nornir, pyATS, Netmiko, Napalm, etc.).

As an automation framework with broad community support and backed by RedHat there are many options we can look at for our use case.

| Option                                                  | Description |
| ------------------------------------------------------- | ----------- |
| Ansible Network Operating System "facts" module         |             |
| Ansible specific modules                                |             |
| Ansible and your own custom parser filter               |             |
| Ansible and Napalm                                      |             |
| Ansible Network Engine Role                             |             |
| Ansible just to gather and save the show command output |             |





There are Ansible "facts" modules for some network operating systems.  These "facts" modules mimic the Ansible facts module that is run by default agains a server to gather facts about that host (name, software version, interfaces, hardware, etc.) and they return structured data.

Example of the structured data returned by the Ansible iOS-facts module

```
root@38c3258b2fd7:/ansible_local/cisco_ios# ansible-playbook -i hosts ios_facts_lab.yml

PLAY [Collect device facts with the ios_facts module and display selected values] ********************************************************************

TASK [Gather Facts with the facts module] ************************************************************************************************************

ok: [ios-xe-mgmt.cisco.com]

TASK [debug] *****************************************************************************************************************************************
ok: [ios-xe-mgmt.cisco.com] => {
    "facts_output": {
        "ansible_facts": {
            "ansible_net_all_ipv4_addresses": [
                "10.10.20.48",
                "10.255.255.1",
                "10.255.255.2",
                "10.10.10.1"
            ],
            "ansible_net_all_ipv6_addresses": [],
            "ansible_net_api": "cliconf",
            "ansible_net_filesystems": [
                "bootflash:"
            ],
            "ansible_net_filesystems_info": {
                "bootflash:": {
                    "spacefree_kb": 5872952.0,
                    "spacetotal_kb": 7712692.0
                }
            },
            "ansible_net_gather_network_resources": [],
            "ansible_net_gather_subset": [
                "hardware",
                "interfaces",
                "default"
            ],
            "ansible_net_hostname": "csr1000v",
            "ansible_net_image": "bootflash:packages.conf",
            "ansible_net_interfaces": {
                "GigabitEthernet1": {
                    "bandwidth": 1000000,
                    "description": "MANAGEMENT INTERFACE - DON'T TOUCH ME",
                    "duplex": "Full",
                    "ipv4": [
                        {
                            "address": "10.10.20.48",
                            "subnet": "24"
                        }
                    ],
                    "lineprotocol": "up",
                    "macaddress": "0050.56bb.e14e",
                    "mediatype": "Virtual",
                    "mtu": 1500,
                    "operstatus": "up",
                    "type": "CSR vNIC"
```

In our case there is nothing "out of the box" that will help us parse the "show ip route" output we need for our use case, so "some assembly is required" with Ansible.

Parsing with Ansible generally involves the network-engine role.  

An entire [Ansible role](https://linuxacademy.com/blog/linux-academy/ansible-roles-explained/) from Ansible for us network types on top of the many Network modules available to us



Ansible's network-engine role and command parser



[INTRODUCING ANSIBLE NETWORK ENGINE ROLE FOR NETWORK AUTOMATION](https://www.ansible.com/introducing-ansible-network-engine-role)  2018-Ansible Fest

[Network Features Coming Soon in Ansible Engine 2.9](https://www.ansible.com/blog/network-features-coming-soon-in-ansible-engine-2.9)

[Ansible Module Index](https://docs.ansible.com/ansible/latest/modules/modules_by_category.html)

Ansible role repository - [Ansible Galaxy](https://galaxy.ansible.com/) 

[Ansible Network Engine and NTC Templates](https://www.josh-v.com/blog/2019/01/27/ansible-network-engine-ntc-templates.html) 

[Part1 of a 2 part blog on using the Ansible network-engine's command parser](https://termlen0.github.io/2018/06/26/observations/) by termlen0





##### Recommended Reading

[How to automate your network using Ansible and NAPALM – Part 1](https://www.agileintegratedsolutions.com/how-to-automate-your-network-using-ansible-and-napalm-part-1/)









Whichever method you chose





Parsing the Data









