import socket, subprocess,sys
from datetime import datetime
import nmap

class PortScanner():

    def __init__(self, ip):
        print("Scanning Host {}".format(ip))
        self.scan(ip)
    
    def scan(self,ip):
        rmip = ip
        try:
            r1 = int(input("Enter the starting port number: "))
            r2 = int (input("Enter the last port number: "))
        except ValueError:
            print("The inserted value is not an acceptable input please select one of the options above")
            self.scan(ip)
        except Exception as e:
            print("Something went wrong \nLeaving...{}".format(e))
            sys.exit()
        self.nmapScan(ip,r1,r2)
    
    def nmapScan(self,ip,sp,ep):
        subprocess.call('clear',shell=True)
        nmScan = nmap.PortScanner()

        # scan localhost for ports in range 21-443
        ports = '{}-{}'.format(sp,ep)
        print('Starting scan...This might take a while')
        nmScan.scan(ip, '10-1000')
        print(nmScan.scaninfo())
        # run a loop to print all the found result about the ports
        for host in nmScan.all_hosts():
            print('Host : %s (%s)' % (host, nmScan[host].hostname()))
            print('State : %s' % nmScan[host].state())
            for proto in nmScan[host].all_protocols():
                print('----------')
                print('Protocol : %s' % proto)
                lport = nmScan[host][proto].keys()
                sorted(lport)
                for port in lport:
                    print ('port : %s\tstate : %s\tservice : %s' % (port, nmScan[host][proto][port]['state'],nmScan[host][proto][port]['product']))