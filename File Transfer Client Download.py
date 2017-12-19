import socket
import pickle
from threading import Thread
from os import fsync
try:
    from Tkinter import *
    from tkMessageBox import *
    from tkFileDialog import *
except:
    from tkinter import *
def dl(sock):
    global current_file_sel,master
    fn_parts = current_file_sel.get().split('.')
    fn = asksaveasfilename(defaultextension=fn_parts[1],filetypes=[('.' + fn_parts[1] + ' Files', '.' + fn_parts[1]), ('All Files', '*.*')])
    def run(s):
        if len(fn) != 0:
            s.send(current_file_sel.get())
            d = s.recv(2048)
            if d != b'FNF':
                with open(fn, 'wb') as f:
                    still_data = True
                    while still_data:
                        data = s.recv(2048)
                        if not data:
                            still_data = False
                        f.write(data)
                        f.flush()
                        fsync(f.fileno())
                f.close()
        else:
            return None
    t = Thread(target= lambda:run(sock))
    t.start()
def m(window,file_names,s):
    global master
    master = window
    if len(file_names) != 0:
        current_file_sel.set((file_names[0]))
        apply(OptionMenu,(master,current_file_sel)+tuple(file_names)).pack()
        Button(master,text='Download Selected File!',command=lambda: dl(s)).pack()
    else:
        Label(master,text="Close This Program And Add More Files").pack()
    master.after(10,master.update)

def setup(window,file_names):
    s = socket.socket()
    host = 'IP Address Here'
    port = 9001
    s.connect((host,port))
    global current_file_sel
    current_file_sel = StringVar()
    del file_names[0]
    m(window,file_names,s)
if __name__ == '__main__':
    global current_file_sel
    init = socket.socket()
    host = 'IP Address Here'
    port = 9001
    init.connect((host, port))
    init.send(b'filenames please')
    length_of_data = init.recv(1024)
    filenames = pickle.loads(init.recv(int(length_of_data)))
    init.close()
    root = Tk()
    setup(root,filenames)
    root.mainloop()
