# Python-Port-Scanner

To install required packages, run the following command:
    sudo pip3 install -r requirements.txt

These scripts should be run with python3.

## About
This simple python port scanner runs agains specified hosts and ports, and reports which ports are open.
Open ports are reported both in the command line and in HTML reports generated in a "reports" subdirectory.
These scripts were tested in a Linux environment.

## Running the Scripts
The port scanner may be run from the command line with the following syntax:
```
python pyscanner.py <host> [-p <ports>] [-u]
```
```<host>``` must be one of three things:
1. A single IP address (eg. 123.123.123.123)
2. An IP subnet and mask (eg. 123.123.123.0/24)
3. The name of a .txt file in the same directory. The text file should contain a list of IP addresses to be scanned, separated by newlines.

Use the ```-p``` option to specify ports. ```<ports>``` may be
1. A single port number (eg. 45)
2. A range of ports separated by a hyphen (eg. 1-1000)

If the ```-p``` option is not used, the scanner scans port 80 by default.

TCP ports are scanned by default. Use the ```-u``` option to scan UDP ports. 

Use the ```-t``` option to perform a traceroute on the specified hosts.
Traceroot requires root privilages.

The scanner may also be run from a simple GUI by running 
```
python scanner_gui.py
```