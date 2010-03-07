import os
import sys
import os.path
import getopt
import socket
from threading import Thread

#Need to do some sed'ing at build time
LIBDIR="../../lib"

sys.path.append(LIBDIR)
import apc_utils
import time

class APCServer(Thread):

    def __init__(self):
        self.serversocket=socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.state_status=apc_utils.state_status_1


    def get_state(self):
        """
        get_state: State setting thread
        Will parse the output of apcaccess. Based on the output of it, the server defines the following states:
        1) Battery is greater than 75%
        2) Battery is between 30 and 75%
        3) Battery is between 10 and 30%
        4) Battery is less than 10%
        5) Est Bat runtime is less than 5 Mins.
            
        If state 5 happens at anytime, shutdown will be signaled.
            """
        battery_left=apc_utils.get_bat_left()
        run_time=apc_utils.get_runtime()
        print run_time
        if run_time > 10:
            if battery_left < 10.0:
                state=4
            if battery_left >= 10 and battery_left <=30:
                state=3
            if battery_left > 30 and battery_left <=75:
                state=2
            if battery_left > 75:
                state=1
        else:
            state=5
        return state

    def client_thread(self):
        print "foo"

    def set_states(self):
     #infinite loop. Will be killed by system stuff
        while 1:
            (clientsocket,address)=serversocket.accept()
            if state == 1:
                sleep = 30
                status=apc_utils.state_status_1
            if state == 2:
                sleep = 10
                status=apc_utils.state_status_2
            if state == 3:
                sleep = 5
                status=apc_utils.state_status_3
            if state == 4:
                sleep = 10
                status=apc_utils.state_status_4
            print "Sleeping for: ", sleep
            time.sleep(sleep)
            
    def start_server(self):
        """
        start_server: Fires off the necessary threads
        If in state 1: Server polls UPS every 30 seconds.
        If in state 2: Server polls UPS every 10 seconds.
        If in state 3: Server polls UPS every 5 seconds.
        If in state 4: Server trips shutdowns
        """
######################################################
#            AUTODETECT IP Address somehow...
#            ALSO LOG to syslog and some file
#####################################################

        hostname=apc_utils.server_hostname
        try:
            self.serversocket.bind((hostname,apc_utils.port_number))
        except socket.error, e:
            print e, hostname," Exiting."
            sys.exit(1)
        self.serversocket.listen(apc_utils.max_connections)

        outstr="Binding to "+ hostname+ " on port "
        outstr+=str(apc_utils.port_number)
        print outstr

        state=self.get_state()
        if state == 5:
            print "APC Battery is close to death. Exiting."
            self.state_status=apc_utils.state_status_4

    
######################################################
#            SIGNAL SHUTDOWN
######################################################
        sys.exit(1)
