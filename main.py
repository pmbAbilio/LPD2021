from portscanner.main import PortScanner
from securechat.main import SecureChat
'''
options ={
  "Exit": "Exits the program",
  "Port Scan" : "This option makes a port scan to a remote host, allowing the specification of either scanning all ports or the most common",
  "List On Going Connections" : "Lists all the machine current connections",
  "Safe Chat(Server/Client)" : "Creates a secure chat while being able to be set as a client or server"
}

'''
options = ["Exit", "Port Scan", "List On Going Connections", "Secure Chat"]

class menu():

    def __init__(self):
        print("Security Solution")
        self.listOptions()
        self.awaitInput()
    
    def listOptions(self):
        for index,opt in enumerate(options):
            print("{} --- {}".format(index, opt))
    
    def awaitInput(self):
        try:
            inpt = int(input("Please select a suitable option: "))
        except ValueError:
            print("The inserted value is not an acceptable input please select one of the options above")
            self.awaitInput()
        except:
            print("Something went wrong \nLeaving...")

        if int(inpt) == 0:
            print("Leaving...")

        elif inpt == 1:
            print("Port Scan...")
            ip = input("Remote System IP: ")
            scanner = PortScanner(ip) 
        elif inpt == 3:
            print("Openning chat application...")
            chat = SecureChat()



c = menu()
