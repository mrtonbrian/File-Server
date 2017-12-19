try:
    from Tkinter import *
    from tkFileDialog import *
    from tkMessageBox import *
except:
    from tkinter import *
import socket
from threading import Thread
from os import path
class sendThread(Thread):
    def __init__(self,s):
        Thread.__init__(self)
        self.s = s
    def run(self):
        global fn
        f = open(fn, 'rb')
        self.s.send(f.read())
        f.close()
        showinfo("Upload","Upload Complete")
def open_file():
    global fn,send_butt
    fn = askopenfilename(title='Open File:')
    send_butt.config(state=NORMAL)
def send_file():
    s = socket.socket()
    host = 'IP Address Here'
    port = 9001
    s.connect((host, port))
    s.send(b'to Send File')
    import time
    time.sleep(.5)
    s.send(path.split(fn)[1])
    g = sendThread(s)
    g.start()
def main(master):
    global send_butt
    Button(master,text="Browse...",command=open_file).pack()
    send_butt = Button(master,text='Send File',state=DISABLED,command=send_file)
    send_butt.pack()
if __name__ == '__main__':
    root = Tk()
    main(root)
    root.mainloop()
