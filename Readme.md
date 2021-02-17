To run this program start by running the following commands:

pip install geoip;
pip install reportlab
pip install python-nmap

Then run: python main.py or python3 main.py

Menu 1

You will be presented whith following options:
0 --- Exit
1 --- Port Scan
2 --- List On Going Connections
3 --- Secure Chat
4 --- Parse log file and generate report

if you select the 1 of Menu 1: 

Remote System IP: 
Enter the starting port number: 

Insert the ip of the remote system you wish to scan
Insert the starting port for the range of ports of the scan
Insert the last port for the range of ports of the scan

if you select the 2 of Menu 1:

NOTE: Here the root password of the system in question has to be added in portscanner/main.py
The system will output the ongoing connections on this system

if you select the 3 of Menu 1:

What type of instance do you wish to start(select 1 for server / 2 for client) 
3 - View message file

if you select 1 the server will start listening for client on the localhost server else if you choose 2 i will start as a client and pront the following questions:
lease insert server IP(127.0.0.1): 
Please insert server port:

answer with ip and port of the server

if you select 3 you will be prompted with following question: 
Messages folder: 
Key filename: 

Answer the above with the folder where the messages are stored and with the file of the key.

if you select the 4 of Menu 1:

1 - ssh
2 - ufw
3 - apache
4 - Create report
5 - Export CSV

select the log filetype you wish to parse and it will parse it and load it to the database. If you select 5 it will prompt with the same question above to decide wich filetype you wish to create report or export.



