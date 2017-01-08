#! /usr/bin/env python

# Author: Jian Wang
# Date: 2017-1-7
# Email: wj_hust08@hust.edu.cn

import socket   #for sockets
import sys  #for exit

#create an INET, STREAMing socket
try:
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
   print 'Failed to create socket'
   sys.exit()

print 'Socket Created'

host = 'oschina.net';
port = 80;

try:
   remote_ip = socket.gethostbyname( host )

except socket.gaierror:
   print 'Hostname could not be resolved. Exiting'
   sys.exit()

#Connect to remote server
#s.connect((remote_ip , port))
s.connect(('127.0.0.1', 8888))

print 'Socket Connected to ' + host + ' on ip ' + remote_ip

#message = "GET / HTTP/1.1\r\nHost: oschina.net\r\n\r\n"
message = raw_input("Content:")
try:
   s.sendall(message)
except socket.error:
   print 'Send failed'
   sys.exit()
print s.recv(1024)

s.close()

