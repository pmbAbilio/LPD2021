import re
from databasefiles.main import DataBaseFiles
import sys
from datetime import datetime
from report.main import reportgenerator
import csv
from databasefiles.main import DataBaseFiles
import subprocess

types = ['SSH','UFW','APACHE']

class LogParser():
    """@package docstring
        Class reponsible for processing the log files of each type.
        """

    IP_RE = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    CONNECTIONS = []
    conn = None

    def __init__(self, conn):
        self.conn = conn
        subprocess.call('clear',shell=True)
        while True:
            try:
                print("What type of logs do you wish to process:\n1 - ssh\n2 - ufw\n3 - apache")
                print("4 - Create report")
                print("5 - Export CSV")
                print("6 - Go back")
                inpt = int(input("Select a suitable option: "))
            except ValueError:
                print("It needs to be a number:")
                self.displayOptions()
            except: 
                print("Unknown option, please try again")
                self.__init__(conn)
            if inpt == 1: 
                file_path = input("Please insert the path to the file: ")
                self.parseSshFile(file_path)    
            elif inpt == 2: 
                file_path = input("Please insert the path to the file: ")
                self.parseUfwFile(file_path)
            elif inpt == 3: 
                file_path = input("Please insert the path to the file: ")
                self.parseApacheFile(file_path)
            elif inpt == 4:
                print("This report can only be generated if the database is already populated!")
                print("Whats the type of log you wish to create report of:\n1 - SSH\n2 - UFW\n3 - Apache\n4 - All") 
                try:
                    inpt = int(input("Select a suitable option: "))
                    if inpt == 1: 
                        print("Creating SSH Report")
                        reportgenerator(self.conn, 'SSH')   
                    elif inpt == 2: 
                        print("Creating UFW Report")
                        reportgenerator(self.conn, 'UFW')
                    elif inpt == 3: 
                        print("Creating apache Report")
                        reportgenerator(self.conn, 'APACHE')
                    elif inpt == 4: 
                        print("Creating apache Report")
                        reportgenerator(self.conn, 1)
                except ValueError:
                    print("It needs to be a number:")
                    self.__init__(conn) 
                except:
                    print("Unknown option, please try again")
                    self.__init__(conn)
            elif inpt == 5:    
                print("Whats the type of log you wish to create CSV file of:\n1 - SSH\n2 - UFW\n3 - Apache\n4 - All")
                inpt = int(input("Select a suitable option: "))
                try:
                    if inpt == 1: 
                        self.createCSV('SSH','ssh.csv') 
                    elif inpt == 2: 
                        self.createCSV('UFW','ufw.csv')
                    elif inpt == 3: 
                        self.createCSV('APACHE','apache.csv')
                    elif inpt == 4: 
                        for i in types:
                            self.createCSV(i,i+'.csv') 
                except ValueError:
                    print("It needs to be a number:")
                    self.__init__(conn) 
                except:
                    print("Unknown option, please try again")
                    self.__init__(conn)
            elif inpt == 6:
                raise NameError
            else:
                print("Select on of the options above")

    def createCSV(self, type, filename) :
        tableheader = []
        if type == 'SSH':
            table = 'sshdata'
            tableheader = ['Id','Ip','Date','User','Message']
        elif type == 'UFW':
            table = 'ufwdata'
            tableheader = ['Id','Ip','Date','message']
        elif type == 'APACHE':
            table = 'apachedata'
            tableheader = ['Id','Ip','Date','Url', 'Result Code']
        filter = {"table" : table, "atribute" : 1}
        
        data = DataBaseFiles.selectdata(self.conn,filter)  

        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(tableheader)
            writer.writerows(data)
        print('{} created in the root Directory'.format(filename))

    def parseSshFile(self,file_path):
        rhosts = r'rhost=.*'
        re_user = r'invalid user.*'
        print("Parsing the file {}...".format(file_path))
        f = open(file_path, 'r')
        host = ''
        date = ''
        user = ''
        line_index = 0
        for index,line in enumerate(f):
            if 'authentication failure' in line:
                line_index = index                
                hosts_raw = re.findall(rhosts, line)
                if len(hosts_raw) > 0:
                    host = hosts_raw[0].split('=')[1].split(' ')[0]
                date = datetime.strptime(' '.join(line.split(' ')[0:3]), '%b %d %H:%M:%S')
                
            if index == line_index + 1:
                users_raw = re.findall(re_user, line)
                if len(users_raw) > 0:
                    user = users_raw[0].split(' ')[2:3][0]
                message = line.split(':')[3:]

            if index == line_index + 2:
                values = (str(host), str(date), str(user),str(message))
                DataBaseFiles.insertsshdata(self.conn, values)
                #print('Attempted login on {} by the host {} with the following user {}'.format( str(date), str(host), str(user)))  
        print("File processed...")         
                
    def parseUfwFile(self, file_path):
        print("Parsing the file {}...".format(file_path))
        f = open(file_path, 'r')
        for line in f:
            ips = re.findall(self.IP_RE, line)
            src_ip = ''
            if len(ips) >= 1:
                date = datetime.strptime(' '.join(line.split(' ')[0:3]), '%b %d %H:%M:%S')
                if len(ips) == 1:
                    src_ip = ips[0]
                elif len(ips) == 2:
                    src_ip = ips[0]
                else:
                    src_ip = 'nf'
                message = line.split(':')[3:]
                values = (str(src_ip), str(date),  str(message))
                print('Connection attemp on {} by the ip {} '.format(str(date), str(src_ip)))
                DataBaseFiles.insertdata(self.conn, values)   
                
        print("File processed...")    

    def parseApacheFile(self, file_path):
        print("Parsing the file {}...".format(file_path))
        f = open(file_path, 'r')
        for line in f:
            ip = line.split(' ')[0]
            d = datetime.strptime(line.split('[')[1].split(']')[0].split(' ')[0], "%d/%b/%Y:%H:%M:%S")
            
            endpoint_raw = line.split(' ')[6:7][0]
            result_code = line.split(' ')[8:9][0]
            #print('IP {} tried to access the following endpoint {} on the following date {} CODE: {}'.format(str(ip), str(endpoint_raw), str(d), str(result_code)))
            values = (str(ip), str(d),  str(endpoint_raw),str(result_code))
            DataBaseFiles.insertapachedata(self.conn, values) 
    

