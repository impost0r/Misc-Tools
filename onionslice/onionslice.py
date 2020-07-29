# -*- coding: utf8 -*-
#!/usr/bin/python
#Onionslice
#Uses Shodan API to map SSH fingerprint(s) to IP(s)


import shodan
import sys
import threading
import Queue

API_KEY = "Sorry, but your Shodan API key is in another castle."
api = shodan.Shodan(API_KEY)

if len(sys.argv) <3:
    print "Please input a filename and the number of threads."
    sys.exit(0)

fingerSalad = []
filename = sys.argv[1]
threads = sys.argv[2]

with open(filename, "rb") as f:
    fingerSalad = f.readlines()
    f.close()

q = Queue.Queue()
for finger in fingerSalad:
    q.put(finger)

def worker(queue):
    queueFull = True
    while queueFull:
        try:
                finger = queue.get(False)
                finger = finger.replace('\r', '').replace('\n', '')
                results = api.search(finger)
                for i in results['matches']:
                    with open('publickeymatch', 'a+') as pKeys:
                        pKeys.write(i['ip_str'] + ':' + finger + '\n')
                        pKeys.close()
                        print "Found IP {0} for key {1}".format(i['ip_str'], finger)
        except Queue.Empty:
                queueFull = False
        except Exception as e:
                print e



for i in range(int(threads)):
    t = threading.Thread(target=worker, args = (q,))
    t.start()
