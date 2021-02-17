from portscanner.main import PortScanner
from securechat.main import SecureChat
from databasefiles.main import DataBaseFiles
from logparser.main import LogParser
from servicescanner.main import servicescanner
import subprocess

options = ["Exit", "Port Scan", "List On Going Connections", "Secure Chat","Parse log file and generate report"]

class menu():
    conn = None

    def __init__(self):

        subprocess.call('clear',shell=True)
        print("Security Solution")
        self.conn = DataBaseFiles.createdatabase()
        self.listOptions()
        self.awaitInput()
    
    def listOptions(self):
        for index,opt in enumerate(options):
            print("{} --- {}".format(index, opt))
    
    def awaitInput(self):
        inpt = None
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
            try:
                scanner = PortScanner(ip) 
            except NameError:
                self.__init__()
        elif inpt == 2:
            try:
                servicescanner()
            except NameError:
                self.__init__()
        elif inpt == 3:
            print("Openning chat application...")
            try:
                chat = SecureChat()
            except NameError:
                self.__init__()
        elif inpt == 4:
            try:
                LogParser(self.conn)
            except NameError:
                self.__init__()




c = menu()
