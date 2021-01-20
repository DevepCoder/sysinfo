import argparse
import sys
import platform
import socket
import os
import re
import json
import uuid 
import psutil


class SystemInfo:
    def getSystemName(): return platform.system()
    def getSystemRelease(): return platform.release()
    def getSystemVersion(): return platform.version()
    def getSystemArchitecture(): return platform.architecture()[0]
    def getProcessor(): return platform.processor()
    def getHostname(): return socket.gethostname()
    def getIpAddress(): return socket.gethostbyname(socket.gethostname())
    def getMacAddress(): return ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    def getUsername(): return os.getenv('USERNAME')
    def getRam(StorageType='GB'):
        if StorageType.lower() == 'gb':
            return str(round(psutil.virtual_memory().total / (1024.0 **3)))
        elif StorageType.lower() == 'mb':
            return str(round(psutil.virtual_memory().total / (1024.0 **2)))
        elif StorageType.lower() == 'kb':
            return str(round(psutil.virtual_memory().total / (1024.0 **1)))
    def getAll():
        sysinfo={
            "username": os.getenv('USERNAME'),
            "platform": platform.system(),
            "platform-release": platform.release(),
            "platform-version": platform.version(),
            "architecture": platform.machine(),
            "hostname": socket.gethostname(),
            "ip-address": socket.gethostbyname(socket.gethostname()),
            "mac-address": ':'.join(re.findall('..', '%012x' % uuid.getnode())),
            "processor": platform.processor(),
            "ram": str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        }
        return json.dumps(sysinfo, indent=4)

def main():
    parser = argparse.ArgumentParser(description='A simple application to get system info(basically like uname but cross-platform)')
    parser.add_argument('--all', '-a', action='store_true', help='prints all information')
    parser.add_argument('--operating-system', '-o', action='store_true', help='prints the system name')
    parser.add_argument('--nodename', '-n', action='store_true', help='prints the network host name')
    parser.add_argument('--sysrelease', '-r', action='store_true', help='prints the system release')
    parser.add_argument('--sysversion', '-sv', action='store_true', help='prints the system version')
    parser.add_argument('--machine', '-m', action='store_true', help='prints the system hardware name')
    parser.add_argument('--processor', '-p', action='store', help='prints the processor model name')
    parser.add_argument('--hardware-platform', '-i', action='store_true', help='prints the system platform (non-portable)')
    parser.add_argument('--username', '-u', action='store_true', help='prints the username')
    parser.add_argument('--ram', '-rm', action='store', choices=['gb', 'mb', 'kb'],help='prints the ram')
    sys.argv.pop(0)
    args = parser.parse_args(sys.argv)
    if len(sys.argv) == 0:
        parser.print_help()
    conditional_dict = {
        'operating_system': SystemInfo.getSystemName(),
        'machine': SystemInfo.getSystemArchitecture(),
        'hardware-platform': SystemInfo.getSystemArchitecture(),
        'sysrelease': SystemInfo.getSystemRelease(),
        'sysversion': SystemInfo.getSystemVersion(),
        'ip_address': SystemInfo.getIpAddress(),
        'mac_address': SystemInfo.getMacAddress(),
        'processor': SystemInfo.getProcessor(),
        'ram': SystemInfo.getRam(args.ram or 'gb'),
        'username': SystemInfo.getUsername(),
        'nodemon': SystemInfo.getHostname(),
        'all': SystemInfo.getAll()
    } 
    for h in args.__dict__.keys():
        if args.__dict__[h]:
            print(conditional_dict[h])
    

main()
