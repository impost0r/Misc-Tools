#!/usr/bin/python
# -*- coding: utf8 -*-
# symfind 
# finds Linux kernel symbols
import platform
import sys
import os
import optparse 

krnvrs = platform.release()
sysmap = ['/boot/System.map-' + krnvrs, 
	'/usr/src/linux/System.map-' + krnvrs, 
	'/lib/modules/System.map-' + krnvrs,
    '/System.map',
    '/System.map-' + krnvrs,
    '/System.map-genkernel-' + krnvrs + '-' + krnvrs,
    '/usr/src/linux-' + krnvrs + '/System.map',
    '/lib/modules/' + krnvrs + '/System.map',
    '/usr/src/linux/System.map',
    '/boot/System.map']
vmlinux = ['/boot/vmlinux', 
	'/usr/src/linux/vmlinux', 
	'/lib/modules/vmlinux', 
	'/usr/lib/debug/vmlinux',
    '/boot/vmlinux-' + krnvrs,
    '/boot/.debug/vmlinux-' + krnvrs,
    '/boot/.debug/vmlinux-' + krnvrs + '.debug',
    '/lib/modules/' + krnvrs + '/vmlinux',
    '/lib/modules/' + krnvrs + '/vmlinux.debug',
    '/lib/modules/' + krnvrs + '/.debug/vmlinux',
    '/lib/modules/' + krnvrs + '/.debug/vmlinux.debug',
    '/usr/lib/debug/lib/modules/' + krnvrs + '/vmlinux',
    '/usr/lib/debug/lib/modules/' + krnvrs + '/vmlinux.debug',
    '/usr/lib/debug/boot/vmlinux-' + krnvrs,
    '/usr/lib/debug/boot/vmlinux-' + krnvrs + '.debug',
    '/usr/lib/debug/vmlinux-' + krnvrs,
    '/usr/lib/debug/vmlinux-' + krnvrs + '.debug',
    '/var/cache/abrt-di/usr/lib/debug/lib/modules/' + krnvrs + '/vmlinux',
    '/var/cache/abrt-di/usr/lib/debug/lib/modules/' + krnvrs + '/vmlinux.debug',
    '/var/cache/abrt-di/usr/lib/debug/boot/vmlinux-' + krnvrs,
    '/var/cache/abrt-di/usr/lib/debug/boot/vmlinux-' + krnvrs + '.debug',
    '/usr/src/linux-' + krnvrs + '/vmlinux',
    '/usr/src/linux/vmlinux',
    '/boot/vmlinux']

desc="""
This is Symfind, a script for finding Linux kernel symbols. 
If you want to supress output and only get the kernel symbol -- pipe the script to grep."""
parser = optparse.OptionParser(description=desc)
parser.add_option('-a', '--all', help='Print all kernel symbols matching sys.argv[1]', dest='pall', default=False, action='store_true')

(opts, args) = parser.parse_args()

def log(message, symbol="+"):
    print("[{0}] {1}".format(symbol, message))

def symhunt(): 
    for map_name in sysmap:
        if not os.path.exists(map_name):
            log("Kernel symbols at {0} do not exist, continuing".format(map_name), symbol="-")
            continue
        try:
            fd = open(map_name, "r")
            kernel_symbols = fd.readlines()
            
        except:
            log("Unable to find/read kernel symbols at {0}".format(map_name), symbol="-")
            continue
        log("Found kernel symbols at {0}".format(map_name))
        for item in kernel_symbols:
            if quere in item:
                log("Found {0}".format(item))
                if not opts.pall == True:
                    sys.exit(0)
        sys.exit(0)

                

    for lindir in vmlinux: 
        if not os.path.exists(lindir):
            log("vmlinux at {0} does not exist, continuing".format(lindir), symbol="-")
            continue
        try:
            os.system("nm {0} &> {1}".format(lindir, ".sysmap"))
        except:
            log("Unable to find/read kernel symbols at {0}".format(lindir), symbol="-")
            continue
        log("Found vmlinux at {0}".format(lindir))
        for linitem in linbuf:
            if quere in linitem:
                log("Found {0}".format(linitem))
                if not opts.pall == True:
                     sys.exit(0)
        sys.exit(0)


if len(sys.argv) < 2:
    log("Please input a symbol!", "-")
    sys.exit(0)

quere = sys.argv[1]

symhunt()

