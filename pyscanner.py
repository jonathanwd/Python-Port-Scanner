#!/usr/bin/env python
# Code that helped me: https://gist.github.com/TheZ3ro/7255052

from threading import Thread
from multiprocessing.dummy import Pool as ThreadPool 
from yattag import Doc
import argparse
import socket
import datetime
import os

host = ""
portstring = ""
counting_open = []
counting_close = []
threads = []

def generate_html(ports):
	f = open("report.html", "w")
	time = datetime.datetime.now()
	doc, tag, text = Doc().tagtext()
	with tag('html'):
		with tag('body'):
			with tag('h1'):
				text('Port Scan Report')
			with tag('p'):
				text("Report generated " + str(time))
			with tag('h3'):
				text("Host: " + host)
			with tag('h3'):
				text("Ports Scanned: " + portstring)
			with tag('h3'):
				text("Open ports: " + str(ports))
	f.write(doc.getvalue())

def scan_tcp(port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = s.connect_ex((host,port))
	if result == 0:
		counting_open.append(port)
		print("Connection to " + host + " " + str(port) + " port [tcp/*] succeeded!")
		s.close()
	else:
		counting_close.append(port)
		s.close()

def scan_udp(port):
	result = os.system("nc -vnzu " + host + " " + str(port))
	if result == 0:
		counting_open.append(port)

def main():
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('host', metavar='123.123.123.123', help='specifies the host to be scanned')
	parser.add_argument('-p', '--ports', metavar='1-1023', default=80, help='specifies the host ports to be scanned')
	parser.add_argument('-u', '--udp', action='store_true', help='performs udp scan instead of tcp scan')
	args = parser.parse_args()
	
	global host
	host = args.host
	scan = scan_tcp
	if args.ports:
		global portstring
		portstring = args.ports
		ports = args.ports.split('-')
		from_port = int(ports[0])
		to_port = int(ports[-1])
	if args.udp:
		scan = scan_udp

	pool = ThreadPool(100)
	pool.map(scan, range(from_port, to_port+1))
	counting_open.sort()

	print("Open ports: " + str(counting_open))
	generate_html(counting_open)

main()

# 40- Command line switches allowing specification of host and port. Also presents simple response to user
# 10- Allow multiple ports to be specified. 
# 10- HTML report
