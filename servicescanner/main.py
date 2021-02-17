import subprocess
import os
import sys


class servicescanner():
    sudoPassword = 'root'
    
    def __init__(self):
        print('Checking for ongoing connections') 
        p = os.system('echo %s|sudo -S %s' % (self.sudoPassword, 'ss -antp'))
        print(p)
        inpt = str(input("Do you wish to go back to the previous menu?(Y/N)"))
        if inpt == 'Y':
            raise NameError
        else:
            sys.exit()
