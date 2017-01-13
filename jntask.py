#! /usr/bin/env python

# Author: Jian Wang
# Date: 2017-1-7
# Email: wj_hust08@hust.edu.cn

import socket   #for sockets
import sys  #for exit

def socket_create():
   return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def socket_connect(s, addr):
   s.connect(addr)
 
def socket_bind(s, addr):
   try:
      s.bind(addr)
   except socket.error, msg:
      print 'Bind failed. Error Code ' + str(msg[0]) + ': ' + msg[1]
      sys.exit()
 
def socket_listen(s, n):
   s.listen(n)

def socket_send(s, m):
   try:
      s.sendall(m)
   except socket.error:
      print 'Send failed'
      sys.exit()

def socket_recv(s, n):
   return s.recv(n)

if __name__ == '__main__':
   s = socket_create()
   socket_connect(s, ('127.0.0.1', 8888))
   socket_send(s, sys.argv[1])
   print socket_recv(s, 1024)
   s.close()

