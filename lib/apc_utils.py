#-*- mode:python -*-
'''
apc_utils.py

utilities that are used by both the client and the server.
'''

import subprocess
import os
import sys

state_status_1="Green"
state_status_2="Yellow"
state_status_3="Orange"
state_status_4="Red"

#Should read these in from a config file
max_connections=10
port_number=51114
server_hostname="192.168.1.107"

def populate_ups_data():
    p=""
    p= subprocess.Popen("apcaccess",stdout=subprocess.PIPE).communicate()[0]
    ups_data=p.strip().splitlines()
#    print ups_data
    return ups_data
    
def lookup_ups_data(data_item):
    p_list=populate_ups_data()
    item=""
    val=""
    for x in p_list:
        item=x.split(":")[0].strip()
        val=x.split(":")[-1].strip()
        #print item,val
        if item == data_item:
            return val

#Parse on the output of apcaccess. Eventually should swig the 
#APCUPSD C API.
def get_bat_left():
    bat_left=lookup_ups_data("BCHARGE")
    return float(bat_left.split()[0])

def get_runtime():
    r_time=lookup_ups_data("TIMELEFT")
    return float(r_time.split()[0])
    
