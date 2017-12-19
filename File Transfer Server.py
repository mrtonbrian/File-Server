#!/usr/bin/python
import socket
from threading import Thread
from SocketServer import ThreadingMixIn
from os import listdir,fsync
import pickle
p = 9001
def get_ip():
    import netifaces as ni
    return str(ni.ifaddresses('eth0')[ni.AF_INET][0]['addr'])
ip = get_ip()
print ip
listen_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listen_sock.bind((ip,p))
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

class sendClient(Thread):
    def __init__(self,addr,port,sock,fn):
        Thread.__init__(self)
        self.addr = addr
        self.port = port
        self.sock = sock
        self.fn = fn
    def run(self):
        try:
            f = open(self.fn,'rb')
            f_dat = f.read(2048)
            self.sock.send(b'good')
            while f_dat:
                self.sock.send(f_dat)
                f_dat = f.read(2048)
                if not f_dat:
                    f.close()
                    self.sock.close()
                    break
        except IOError:
            #FNF = File Not Found
            self.sock.send(b'FNF')
            self.sock.close()

class recvClient(Thread):
    def __init__(self,s):
        Thread.__init__(self)
        self.s = s
    def run(self):
        fn = self.s.recv(2048)
        with open(fn, 'wb') as f:
            still_data = True
            while still_data:
                data = self.s.recv(2048)
                #print 'data',data
                if not data:
                    still_data = False
                f.write(data)
                f.flush()
                fsync(f.fileno())
        f.close()

while True:
    try:
        listen_sock.listen(5)
        print 'Waiting...'
        conn, (ip,port) = listen_sock.accept()
        file_name_sent = conn.recv(1024)
        print 'Connection', (ip,port), 'Wants',file_name_sent
        if file_name_sent == b'filenames please':
            files = listdir('.')
            data = pickle.dumps(files)
            conn.send(str(len(data)))
            conn.send(data)
        elif file_name_sent == b'to Send File':
            new_t = recvClient(conn)
            new_t.start()
        else:
            new_t = sendClient(ip,port,conn,file_name_sent)
            new_t.start()
    except:
        pass
