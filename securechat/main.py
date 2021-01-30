import socket, subprocess,sys
from securechat.server import server
from securechat.client import client


class SecureChat():

    def __init__(self):
        self.displayOptions()        

    def displayOptions(self):
        try:
            inpt = int(input("What type of instance do you wish to start(select 1 for server / 2 for client): "))
        except ValueError:
            print("It needs to be a number:")
            self.displayOptions()
        except: 
            print("Unknown option, please try again")
            self.displayOptions()
        if inpt == 1: self.startServer()
        elif inpt == 2: self.startClient()
        else: sys.exit()
        

    def startServer(self):
        connected_server = server()
    def startClient(self):
        server_ip = input("Please insert server IP(127.0.0.1): ")
        try:
            server_port = int(input("Please insert server port: "))
        except ValueError:
            print("It needs to be a number:")
            self.displayOptions()
        except: 
            print("Unknown option, please try again")
            self.displayOptions()
        connected_client = client(server_ip, server_port)
