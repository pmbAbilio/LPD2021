import re
from databasefiles.main import DataBaseFiles
import sys
from datetime import datetime



config = {'ssh':
                {'filename': 'auth.log',
                'Date':[0,3],
                'Message':'',
                'Address':'',
                }
        }

class LogParser():
    IP_RE = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    CONNECTIONS = []
    conn = None

    def __init__(self, conn):
        self.conn = conn
        print('Please note that it is only possible to parse apache and ufw log files.')
        try:
            print("What type of logs do you wish to process\n1 - for ssh\n2 - ufw\n3 - apache\n")
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
        else: sys.exit()

        

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
                date = ' '.join(line.split(' ')[0:3])
                
            if index == line_index + 1:
                users_raw = re.findall(re_user, line)
                if len(users_raw) > 0:
                    user = users_raw[0].split(' ')[2:3][0]
                message = line.split(':')[3:]

            if index == line_index + 2:
                #values = ('UFW',str(ip), str(date),  str(message))
                #DataBaseFiles.insertdata(self.conn, values)
                print('Attempted login on {} by the host {} with the following user {}'.format( str(date), str(host), str(user)))           
                
    def parseUfwFile(self, file_path):
        print("Parsing the file {}...".format(file_path))
        f = open(file_path, 'r')
        for line in f:
            ips = re.findall(self.IP_RE, line)
            src_ip = ''
            if len(ips) >= 1:
                date = ' '.join(line.split(' ')[0:3])
                if len(ips) == 1:
                    src_ip = ips[0]
                elif len(ips) == 2:
                    src_ip = ips[0]
                else:
                    src_ip = 'nf'
                message = line.split(':')[3:]
                #values = ('UFW',str(ip), str(date),  str(message))
                print('Connection attemp on {} by the ip {} '.format(str(date), str(src_ip)))
                #print(DataBaseFiles.insertdata(self.conn, values))    
                #print(date)

    def parseApacheFile(self, file_path):
        print("Parsing the file {}...".format(file_path))
        f = open(file_path, 'r')
        for line in f:
            ip = line.split(' ')[0]
            
            date = line.split('[')[1].split(']')[0]
            d = datetime.strptime(date, "%d/%b/%Y:%H:%M:%S %z")
            
            endpoint_raw = line.split(' ')[6:7][0]
            result_code = line.split(' ')[8:9][0]
            print('IP {} tried to access the following endpoint {} on the following date {} CODE: {}'.format(str(ip), str(endpoint_raw), str(d), str(result_code)))
                #values = ('UFW',str(ip), str(date),  str(message))
                #print(values)
                #print(DataBaseFiles.insertdata(self.conn, values))    
                #print(date)

