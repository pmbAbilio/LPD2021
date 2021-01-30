import re
from databasefiles.main import DataBaseFiles

class LogParser():
    IP_RE = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    CONNECTIONS = []
    conn = None

    def __init__(self, conn):
        self.conn = conn
        file_path = input("Plese insert the path to the file or the name is its on the project folder: ")
        self.parsefile(file_path)

    def parsefile(self,file_path):
        print("Parsing the file {}...".format(file_path))
        f = open(file_path, 'r')
        for line in f:
            ips = re.findall(self.IP_RE, line)
            ip = ''
            if len(ips) >= 1:
                date = ' '.join(line.split(' ')[0:3])
                if len(ips) == 1:
                    ip = ips[0] 
                message = line.split(':')[3:len(line.split(':'))-1]
                values = (str(ip), str(date),  str(message))
                print(values)
                print(DataBaseFiles.insertdata(self.conn, values))    
                print(date)
