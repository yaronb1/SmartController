import socket
import sys


class PiController():
    def __init__(self,
                 host = '',
                 port= 9999,
                 close=False,
                 connect=True
                 ):

        self.host = host
        self.port = port

        if connect:
            try:self.s = socket.socket()
            except socket.error as msg:
                print("Socket creation error: " + str(msg))


            try: self.close_socket()
            finally:
                if close:
                    pass
                else:
                    try:
                        self.bind_socket()
                        self.socket_accept()
                    finally: self.close_socket()
            #self.close_socket()


    # Binding the socket and listening for connections
    def bind_socket(self):
        try:
            print("Binding the Port: " + str(self.port))

            self.s.bind((self.host, self.port))
            self.s.listen(5)

        except socket.error as msg:
            print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
            self.bind_socket()


# Establish connection with a client (socket must be listening)

    def socket_accept(self):
        self.conn, address = self.s.accept()
        print("Connection has been established! |" + " IP " + address[0] + " | Port" + str(address[1]))


    def close_socket(self):
        try:
            self.conn.close()
            self.s.close()
        except:pass


    # Send commands to client/victim or a friend
    def send_commands(self,cmd):
        if len(str.encode(cmd)) > 0:
            self.conn.send(str.encode(cmd))
            # client_response = str(self.conn.recv(1024),"utf-8")
            # print(client_response)


if __name__ =="__main__":
    pi = PiController(close=True)
