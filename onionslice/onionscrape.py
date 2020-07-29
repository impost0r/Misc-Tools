import paramiko
import socket
import hashlib
import sys
import threading
import Queue
import socks

serverList = []
portList = []

filename = sys.argv[1]
ports = sys.argv[2]
threads = sys.argv[3]

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
with open(filename, "rb") as f:
    serverList = f.readlines()
    f.close()

with open(ports, "rb") as p:
    portList = p.readlines()
    p.close()
    
q = Queue.Queue()
for server in serverList:
    q.put(server)

def worker(queue):
    queueFull = True
    while queueFull:
        try:
            server = queue.get(False)
            server = server.replace('\r', '').replace('\n', '')
            socket = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM) #change to socks.socksocket if using pysocks
            for port in portList:
                gaysocket.connect((server, int(port)))
        except Queue.Empty:
            queueFull = False
        except socket.error:
            print "Cannot connect to {0}".format(server)
        except socks.SOCKS5Error:
            print "SOCKS Exception"
        except Exception:
            print "Generalized error."

        try:
            transport = paramiko.Transport(gaysocket)
            transport.start_client()
            sshK = transport.get_remote_server_key()
            fingerprint = hashlib.md5(sshK.__str__()).hexdigest()
            printableFinger = ":".join(a+b for a,b in zip(fingerprint[::2], fingerprint[1::2]))
            print printableFinger
            with open('fingers.txt', 'a+') as fingerfile:
                fingerfile.write(printableFinger + '\n')
                fingerfile.close()
        except paramiko.SSHException:
            print "Exception within Paramiko"
        except Exception:
            print "Generalized error."



    transport.close()
    socket.close()

    
    
for i in range(int(threads)):
    t = threading.Thread(target=worker, args = (q,))
    t.start()
