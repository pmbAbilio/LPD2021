from portscanner.main import PortScanner

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
        while True:
            try:
                inpt = int(input("Please select a suitable option: "))
            except ValueError:
                print("The inserted value is not an acceptable input please select one of the options above")
                self.awaitInput()
                break
            except:
                print("Something went wrong \nLeaving...")
                break

            if int(inpt) == 0:
                print("Leaving...")
                break

            elif inpt == 1:
                print("Port Scan...")
                ip = input("Remote System IP: ")
                scanner = PortScanner(ip) 



c = menu()
