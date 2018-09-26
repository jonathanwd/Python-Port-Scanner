#!/usr/bin/env python
# Base code here: https://gist.github.com/TheZ3ro/7255052

from threading import Thread
import argparse
import socket

def parse_args():
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('host', metavar='123.123.123.123', help='specifies the host to be scanned')
	parser.add_argument('-p', metavar='1-1023', help='specifies the host to be scanned')
	args = parser.parse_args()
	print(args.host)

# host = raw_input('host > ')
# from_port = input('start scan from port > ')
# to_port = input('finish scan to port > ')   
counting_open = []
counting_close = []
threads = []

def scan(port):
	s = socket.socket()
	result = s.connect_ex((host,port))
	print('working on port > '+(str(port)))      
	if result == 0:
		counting_open.append(port)
		#print((str(port))+' -> open') 
		s.close()
	else:
		counting_close.append(port)
		#print((str(port))+' -> close') 
		s.close()

parse_args()
# for i in range(from_port, to_port+1):
# 	t = Thread(target=scan, args=(i,))
# 	threads.append(t)
# 	t.start()
	
# [x.join() for x in threads]

# print(counting_open)
	