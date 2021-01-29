import socket
import select

class server():
    HEADER_LENGTH = 10
    IP = '127.0.0.1'
    PORT = 1234
    clients = {}
    def __init__(self):
        self.startServer()
# Handles message receiving
    def receive_message(self, client_socket):

        try:

            # Receive our "header" containing message length, it's size is defined and constant
            message_header = client_socket.recv(self.HEADER_LENGTH)

            # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(message_header):
                return False

            # Convert header to int value
            message_length = int(message_header.decode('utf-8').strip())

            # Return an object of message header and message data
            if client_socket not in self.clients:
                return {'header': message_header, 'key': client_socket.recv(message_length)}
            else:
                return {'header': message_header, 'data': client_socket.recv(message_length)}

        except:

            # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
            # or just lost his connection
            # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
            # and that's also a cause when we receive an empty message
            return False

    def startServer(self):

        # Create a socket
        # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
        # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # SO_ - socket option
        # SOL_ - socket option level
        # Sets REUSEADDR (as a socket option) to 1 on socket
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind, so server informs operating system that it's going to use given IP and port
        # For a server using 0.0.0.0 means to listen on all available interfaces, useful to connect locally to 127.0.0.1 and remotely to LAN interface IP
        server_socket.bind((self.IP, self.PORT))

        # This makes server listen to new connections
        server_socket.listen()

        # List of sockets for select.select()
        sockets_list = [server_socket]

        # List of connected self.clients - socket as a key, user header and name as data
        

        print(f'Listening for connections on {self.IP}:{self.PORT}...')
        while True:

                # Calls Unix select() system call or Windows select() WinSock call with three parameters:
                #   - rlist - sockets to be monitored for incoming data
                #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
                #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
                # Returns lists:
                #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
                #   - writing - sockets ready for data to be send thru them
                #   - errors  - sockets with some exceptions
                # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
                read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

                # Iterate over notified sockets
                for notified_socket in read_sockets:

                    # If notified socket is a server socket - new connection, accept it

                    if notified_socket == server_socket:
                        # Accept new connection
                        # That gives us new socket - client socket, connected to this given client only, it's unique for that client
                        # The other returned object is ip/port set
                        
                        client_socket, client_address = server_socket.accept()
                        
                        if len(self.clients) + 1 <= 2:
                            # Client should send his name right away, receive it
                            user = self.receive_message(client_socket)

                            if user is False:
                                continue

                            # Add accepted socket to select.select() list
                            sockets_list.append(client_socket)

                            user['username'] = 'user'+str(len(self.clients))
                            self.clients[client_socket] = user
                            self.notify_all(client_socket, self.clients)

                            #print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
                            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['username']))
                        else:
                            message = f"Not allowed to connect, too many users already".encode('utf-8')
                            message_header = f"{len(message):<{10}}".encode('utf-8')
                            client_socket.send(message_header + message)
                            client_socket.close()

                    # Else existing socket is sending a message
                    else:
                        # Receive message
                        message = self.receive_message(notified_socket)

                        # If False, client disconnected, cleanup
                        if message is False:
                            print('Closed connection from: {}'.format(self.clients[notified_socket]['username']))
                            #.decode('utf-8')
                            # Remove from list for socket.socket()
                            sockets_list.remove(notified_socket)

                            # Remove from our list of users
                            del self.clients[notified_socket]

                            continue

                        # Get user by notified socket, so we will know who sent the message
                        user = self.clients[notified_socket]
                        #print(user['key'])
                        #print(f'Received message from {user["username"]}: {message["data"].decode("utf-8")}')

                        # Iterate over connected self.clients and broadcast message
                        for client_socket in self.clients:

                            # But don't sent it to sender
                            
                            if client_socket != notified_socket:
                                #print("sending: " + message['data'].decode("utf-8") + " to " + self.clients[client_socket]['username'])
                                # Send header and message
                                client_socket.send(message['header'] + message['data'])

                # It's not really necessary to have this, but will handle some socket exceptions just in case
                for notified_socket in exception_sockets:

                    # Remove from list for socket.socket()
                    sockets_list.remove(notified_socket)

                    # Remove from our list of users
                    del self.clients[notified_socket]

    def notify_all(self, sender, clients):
        for client_socket in clients:
            if clients[client_socket] != clients[sender]:
                print("Sending Key!!")
                sender.send(clients[client_socket]['header'] + clients[client_socket]['key'])
                client_socket.send(clients[sender]['header'] + clients[sender]['key'])
