#!/usr/bin/env python
# Base code here: https://gist.github.com/TheZ3ro/7255052

from threading import Thread
from multiprocessing.dummy import Pool as ThreadPool 
import argparse
import socket

host = ""
counting_open = []
counting_close = []
threads = []

def scan(port):
	s = socket.socket()
	result = s.connect_ex((host,port))
	print('working on port > '+(str(port)))      
	if result == 0:
		counting_open.append(port)
		s.close()
	else:
		counting_close.append(port)
		s.close()

def main():
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('host', metavar='123.123.123.123', help='specifies the host to be scanned')
	parser.add_argument('-p', '--ports', metavar='1-1023', help='specifies the host ports to be scanned')
	args = parser.parse_args()
	
	host = args.host
	if args.ports:
		ports = args.ports.split('-')
		from_port = int(ports[0])
		to_port = int(ports[-1])
	else:
		from_port = 1
		to_port = 1

	pool = ThreadPool(100)
	pool.map(scan, range(from_port, to_port+1))

	print(counting_open)
	print(counting_close)
main()