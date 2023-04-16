import socket
import sys
import json
from hashlib import md5
try:
    import Crypto
    from Crypto.Cipher import AES  # PyCrypto
except ImportError:
    Crypto = AES = None
    import pyaes  # https://github.com/ricmoo/pyaes



#create a scockeT(connecting 2 computers)
def create_socket():
    global host  # ip address
    global port
    global s

    host = "192.168.175.3"
    port = 9999
    try: s = socket.socket()
    except socket.error as msg:
        print('error creating socket ' + str(msg))

#bindong the socket and listenong for connections
def bind_socket():

    try:
        global host
        global port
        global s

        print("binding port " + str(port))

        s.bind((socket.gethostname(),port)) #command to bind socket with device
        s.listen(5) # listen for connections with the number of packets we can tolerate
    except socket.error as msg: # if it was unsuccessful we will try again
        print(str(msg))
        bind_socket()


#establish a connection with a client(socket must be listening)
def socket_accept():
    conn, address = s.accept() # will only move to the next line if connection was successful
    print('connection has been established | '  + "IP " + address[0] + " | Port" + str(address[1]))
    send_commands(conn,"")
    conn.close() # close the connection



#send commands to client
def send_commands(conn, cmd):

    if len(str.encode(cmd)) > 0: # the string command will be encoded t bytes
        conn.send(str.encode(cmd))
        client_response = str(conn.recv(1024), "utf-8") #receive a client response with the proper encoding 1024 is the max bytes it will accept
        print(client_response)


def main():
    create_socket()
    bind_socket()
    socket_accept()

udpkey = md5(b"yGAdlopoPVldABfn").digest()


def unpad(s):
    return s[: -ord(s[len(s) - 1 :])]

def decrypt_udp(msg):
    return decrypt(msg, udpkey)

def decrypt(msg, key):
    return unpad(AES.new(key, AES.MODE_ECB).decrypt(msg)).decode()

def start_socket(address,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    print('attempting to connect')
    try:
        print('trying')
        s.connect((address, port))
        print("succeeded")
        s.close()
    except Exception as e:
        print("failed " + str(e))
        start_socket(address,port)

def start_socket2(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(),port))
    s.listen(5)

    while True:
        clientsocket, address = s.accept()
        print("connection has been established from"  + str(address))

#start_socket2(6668)
## need to try both methods (but especia;;;y strat_socket) with a device already
## been linked with tuya
from kasa import Discover, SmartBulb, SmartPlug
devices = await Discover.discover()
for addr, dev in devices.items():
    await dev.update()
    print(addr)