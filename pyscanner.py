#!/usr/bin/env python

from threading import Thread
from multiprocessing.dummy import Pool as ThreadPool 
from yattag import Doc
from netaddr import IPNetwork
from scapy.all import *
import argparse
import socket
import datetime
import os
import webbrowser

host = ""
portstring = ""
counting_open = []
threads = []

# Create an HTML report is created for every valid IP address scanned.
def generate_html(ports, protocol):
	if not os.path.exists("reports"):	
		os.makedirs("reports") 												# Create the 'reports' subdirectory if it does not exist
	filename = host + "-report.html"
	f = open(os.path.join("reports",filename), "w")
	time = datetime.datetime.now()
	doc, tag, text = Doc().tagtext()
	with tag('html'):
		with tag('body'):
			with tag('h1'):
				text(protocol + ' Port Scan Report')
			with tag('p'):
				text("Report generated " + str(time))
			with tag('h3'):
				text("Host: " + host)
			with tag('h3'):
				text("Ports Scanned: " + portstring)
			with tag('h3'):
				text("Open ports: " + str(ports))
	f.write(doc.getvalue())
	webbrowser.open('file://' + os.path.realpath("reports/" + filename))	# This line opens the HTML report in the user's default browser

# Scans a single TCP port
def scan_tcp(port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = s.connect_ex((host,port))
	if result == 0:
		counting_open.append(port)
		print("Connection to " + host + " " + str(port) + " port [tcp/*] succeeded!")
		s.close()
	else:
		s.close()

# Scans a single UDP port
def scan_udp(port):
	result = os.system("nc -vnzu " + host + " " + str(port))
	if result == 0:
		counting_open.append(port)

# Performs traceroute on an IP address
def traceroute(port):
	result, unans = scapy.all.traceroute(host,maxttl=32)
	print(result)

# Turns the host argument into a list of hosts to scan
def generate_hosts(host_arg):
	hosts = []
	if "txt" in host_arg:					# Reads IP addresses to scan from a file
		f = open(host_arg, "r")
		hosts = f.read().split('\n')
	elif("/" in host_arg):					# Changes subnet mask into a range of addresses to scan
		for ip in IPNetwork(host_arg):
			hosts.append(str(ip))
	else:
		hosts.append(host_arg)				# Assumes that the host argument is a single IP address to scan
	return hosts

def main():
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('host', metavar='123.123.123.123 or filename.txt', help='specifies the host to be scanned, or the file to read host ips from')
	parser.add_argument('-p', '--ports', metavar='1-1023', default=80, help='specifies the host ports to be scanned')
	parser.add_argument('-u', '--udp', action='store_true', help='performs udp scan instead of tcp scan')
	parser.add_argument('-t', '--traceroute', action='store_true', help='performs traceroute on specified ports')
	args = parser.parse_args()
	
	hosts = generate_hosts(args.host)		# Generate list of IPs to scan

	scan = scan_tcp
	protocol = "TCP"
	print(args)
	if args.ports:
		global portstring
		portstring = str(args.ports)
		ports = portstring.split('-')
		from_port = int(ports[0])
		to_port = int(ports[-1])
	if args.udp:
		protocol = "UDP"
		scan = scan_udp

	for h in hosts:
		print(h)
		HOST_UP  = True if os.system("ping -c 1 " + h) is 0 else False	# Check if host is reachable through ping
		if HOST_UP:
			global host
			host = h
			pool = ThreadPool(100)							# Create 100 threads for scanning
			if args.traceroute:
				scan = traceroute
				pool.map(scan, range(from_port, to_port+1))	
			else:
				pool.map(scan, range(from_port, to_port+1))	
				counting_open.sort()
				print("Open ports: " + str(counting_open))
				generate_html(counting_open, protocol)
				counting_open.clear()
main()
