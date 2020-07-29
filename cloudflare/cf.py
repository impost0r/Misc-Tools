'''
CF.py
Built for Python 2.7.3 (Linux)
Req: netaddr (https://github.com/drkjam/netaddr/)
'''
import socket
import sys
from netaddr import *

if len (sys.argv) < 2:
    print "Supply a domain."
    sys.exit(0)

host = sys.argv[1]
subdomains = ["|", "www", "cpanel", "ftp", "mail", "webmail", "direct", "direct-connect"]
cloudflareranges = [IPNetwork("2400:cb00::/32"), IPNetwork("2606:4700::/32"), IPNetwork("2803:f800::/32"),
                    IPNetwork("2405:b500::/32"), IPNetwork("2405:8100::/32"), IPNetwork("204.93.240.0/24"),
                    IPNetwork("204.93.177.0/24"), IPNetwork("199.27.128.0/21"), IPNetwork("173.245.48.0/20"),
                    IPNetwork("103.22.200.0/22"), IPNetwork("141.101.64.0/18"), IPNetwork("108.162.192.0/18"),
                    IPNetwork("190.93.240.0/20"), IPNetwork("188.114.96.0/20"), IPNetwork("197.234.240.0/22"),
                    IPNetwork("198.41.128.0/17"), IPNetwork("162.158.0.0/15"), IPNetwork("104.16.0.0/12")
                    ]


def isCloudflare(addr):
    for iprange in cloudflareranges:
        if addr in iprange:
            return True
    return False

for x in subdomains:
    fulldomain = host if x == "|" else x + "." + host #| is root domain, just a small check
    prefix = "[{0}]".format(fulldomain)
    try:
        ips = []
        for ip in socket.getaddrinfo(host, 80):
            if ip[4][0] not in ips:
                ips.append(ip[4][0])
        iplist = ", ".join(ip for ip in ips)
        for _ in iplist.split(", "):
            if isCloudflare(_):
                print "{0} is Cloudflared.".format(prefix)
                break
            else:
                print "{0} {1}".format(prefix, iplist)
                break
    except Exception as e:
        print "{0} failed. ({1})".format(prefix, str(e))

