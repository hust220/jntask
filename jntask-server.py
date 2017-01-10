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
import thread

MAX_TASKS = 8
PORT = 8888
LOG_FILE = "/var/log/jntask/tasks.log"

def write_log(str):
   f = open(LOG_FILE, 'a')
   f.write(str)
   f.close()

def tasks_state(tasks):
   return "running: %d, waiting: %d...\n" % (len(tasks['running']), len(tasks['waiting']))

def sub_task(tasks, task):
   write_log(tasks_state(tasks))
   subprocess.call(task['cmd'], shell=True)
   rm_task(tasks['running'], task)
   write_log(tasks_state(tasks))

def start_task(tasks):
   if len(tasks['waiting']) > 0:
      task = tasks['waiting'][0]
      tasks['running'].append(task)
      del tasks['waiting'][0]
      thread.start_new_thread(sub_task, (tasks, task))
   write_log("running: %d, waiting: %d...\n" % (len(tasks['running']), len('waiting')))

def handle_tasks(tasks):
   while True:
      while len(tasks['running']) < MAX_TASKS and len(tasks['waiting']) > 0:
         start_task(tasks)
      time.sleep(3)

def rm_task(tasks, task):
   n = 0
   for t in tasks:
      if t['id'] == task['id']:
         del tasks[n]
         break
      n += 1
   return

def dict_cons(dist_, key_, val_):
   d = {}
   for i in dist_:
      d[i] = dist_[i]
   d[key_] = val_
   return d

def task_find(tasks_, cb_):
   ls = []
   for i in ['running', 'waiting']:
      n = 0
      for j in tasks_[i]:
         if cb_(j):
            t = dict_cons(j, 'state', i)
            if i == 'waiting':
               t['rank'] = n
            ls.append(t)
         n += 1
   return ls

def clientthread(conn, tasks):
   data = conn.recv(1024)
   write_log("recieved: %s\n" % data)
   try:
      if data[0] == 'S':
         task = json.loads(data[1:])
         id = random.randint(1, 999999999)
         conn.sendall(str(id))
         task['id'] = id
         tasks['waiting'].append(task)
      elif data[0] == 'Q':
         query = json.loads(data[1:])
         if 'id' in query:
            id = int(query['id'])
            cb = lambda t : t['id'] == id
         else:
            cb = lambda : True
         matched_tasks = task_find(tasks, cb)
         conn.sendall(json.dumps(matched_tasks))
   except:
      conn.sendall('-1')
   conn.close()

def socket_create():
   return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def socket_bind(s, addr):
   try:
      s.bind(addr)
   except socket.error, msg:
      write_log("Bind Failed. Error code %d: %s\n" % (msg[0], msg[1]))
      sys.exit()

def socket_listen(s, n):
   s.listen(n)

if __name__ == '__main__':
   tasks = {'running':[], 'waiting':[]}
   s = socket_create()
   socket_bind(s, ('', 8888))
   socket_listen(s, 10)

   thread.start_new_thread(handle_tasks, (tasks,))
   while True:
      conn, addr = s.accept()
      write_log("Connected with %s:%d...\n" % (addr[0], addr[1]))
      thread.start_new_thread(clientthread, (conn, tasks))

   s.close()

