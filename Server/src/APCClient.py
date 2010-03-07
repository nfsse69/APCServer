'''
APCClient: Client to connect to the APCServer that is plugged into the USB/serial cable
   for an APC UPS.
Usage:
    APCClient.py -h|--help -w|--windows -l|--linux
    --help: prints this message.
    --windows: runs this as a windows client
    --linux: runs this as a linux client
'''
import os
import sys
import os.path
import getopt

def Usage():
    #Use DOC string for easier stuff.
    print __doc__

#######Main########
start_dir=os.getcwd()
pid= os.getpid()
op_sys_set=1

try:
    opts, args = getopt.getopt(sys.argv[1:], "wlh" ,["windows","linux","help"])
    for o, a in opts:
        if o in ("-h", "--help"):
            Usage()
            sys.exit(2)
        elif o in ("-w", "--windows"):
            op_sys = "windows"
            op_sys_set+=1
        elif o in ("-l", "--linux"):
            op_sys = "linux"
            op_sys_set+=1
        else:
            print "Invalid Usage"
            Usage()
            sys.exit(2)
            
    if op_sys_set > 2:
        print "windows and linux options are mutually exclusive"
        Usage()
        sys.exit(2)
    
except getopt.GetoptError, err:
    print err
    Usage()
    sys.exit(1)
except Exception, e:
    print e
    sys.exit(2)
    

#Need to flesh out what to do here.
if op_sys == "linux":
    print "Run in Linux Mode"
elif op_sys == "windows":
    print "Run in Windows Mode"
