import socket, subprocess,sys
from datetime import datetime


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
        except:
            print("Something went wrong \nLeaving...")
            sys.exit()
        
        subprocess.call('clear',shell=True)
        print("Scanning {} on the following port range [{}, {}]".format(rmip, r1, r2))
        t1= datetime.now()
        try:
            for port in range(r1,r2):
                sock= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                result = sock.connect_ex((rmip,port))
                if result == 0:
                    print ("Port Open:-->\t", port)
                    sock.close()
        except KeyboardInterrupt:
            print ("Stoping Scan ")
            sys.exit()
        except socket.gaierror:
            print ("Hostname could not be resolved")
            sys.exit()
        except socket.error:
            print ("Could not connect to server")
            sys.exit()
        t2= datetime.now()
        total =t2-t1
        print ("scan completed in: {}".format(total))