from tkinter import *
from tkinter.ttk import *
import os 

def clicked():
    lbl_message.configure(text="Scanning started...")
    command = "python3 pyscanner.py " + txt_ip.get() + " -p " + txt_port.get()
    if combo_proto.get() == "udp":
        command += " -u"
    os.system(command)
    lbl_message.configure(text="Scanning complete. HTML reports found in the reporting directory.")

window = Tk()
window.title("Simple Python Port Scanner")
window.geometry('350x200')
lbl_ip = Label(window, text="IP address")
lbl_ip.grid(column=0, row=0)
txt_ip = Entry(window,width=10)
txt_ip.grid(column=1, row=0)
lbl_port = Label(window, text="Port")
lbl_port.grid(column=0, row=1)
txt_port = Entry(window,width=10)
txt_port.grid(column=1, row=1)
lbl_proto = Label(window, text="Protocol")
lbl_proto.grid(column=0, row=2)
combo_proto = Combobox(window, width=9)
combo_proto['values']= ("tcp", "udp")
combo_proto.current(0) 
combo_proto.grid(column=1, row=2)
btn = Button(window, text="Scan", command=clicked)
btn.grid(column=0, row=3)
lbl_message = Label(window, text="")
lbl_message.grid(column=3, row=4)
window.mainloop()