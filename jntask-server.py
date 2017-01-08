#! /usr/bin/env python

# Server of jntask
# Author: Jian Wang
# Date: 2017-1-7
# Email: wj_hust08@hust.edu.cn

import socket
import sys
import json
import subprocess
import random
import time
from thread import *

HOST = ''   
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
   s.bind((HOST, PORT))
except socket.error, msg:
   print 'Bind failed. Error Code ' + str(msg[0]) + ': ' + msg[1]
   sys.exit()

print 'Socket bind complete'

s.listen(10)
print 'Socket now listening'

running_tasks = []
waiting_tasks = []

def start_task(task):
   tasks.append(waiting_tasks[0])
   subprocess.call(task['cmd'], shell=True)

def handle_tasks(running_tasks, waiting_tasks):
   while True:
      l = len(running_tasks)
      n = 8 - l
      while n > 0:
         task = waiting_tasks[0]
         id = task['id']
         running_tasks.append(task)
         rm_task(waiting_tasks, id)
         subprocess.call(task['cmd'], shell=True)
         rm_task(running_tasks, id)
         n -= 1
      time.sleep(3)

def rm_task(tasks, id):
   n = 0
   for t in tasks:
      if t['id'] == id:
         del tasks[n]
         break
      n += 1
   return

def clientthread(conn, running_tasks, waiting_tasks):
   data = conn.recv(1024)
   if data[0:4] == "TASK":
      data = data[4:]
      try:
         task = json.loads(data)
         if task['type'] == 'sub' and 'cmd' in task:
            id = random.randint(1, 999999999)
            conn.sendall(str(id))
            task['id'] = id
            waiting_tasks.append(task)
         elif task['type'] == 'query':
            id = int(task['id'])
            conn.sendall('query')
      except:
         conn.sendall('-1')
         print data
   elif data[0:4] == "FILE":
      pass
   else:
      pass
   conn.close()

start_new_thread(handle_tasks, (running_tasks, waiting_tasks))
while True:
   conn, addr = s.accept()
   print 'Connected with ' + addr[0] + ':' + str(addr[1])
   start_new_thread(clientthread, (conn, running_tasks, waiting_tasks))

s.close()

