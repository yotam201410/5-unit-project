import re
import tkinter
from SQLManagment.SQLClient import SQLClient
from typing import List
from NetworkTalk.MultiSocket import MultiSocket

class GUIClient(object):
    buttons: List[tkinter.Button]
    labels: List[tkinter.Label]

    def __init__(self,sql_client:SQLClient,multi_socket:MultiSocket):
        self.sql_client = sql_client
        self.multi_socket = multi_socket
        self.root = tkinter.Tk(screenName="Guard Client")
        self.buttons = []
        self.labels = []
        self.create_sign_up_page()
        self.main_loop()

    def clear_page(self):
        for i in self.buttons:
            i.destroy()
        for y in self.labels:
            y.destroy()
    def main_loop(self):
        self.root.mainloop()
    def create_sign_up_page(self):
        username_label = tkinter.Label(self.root, width=35, borderwidth=5,text="Username")
        username_label.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        username_entry  = tkinter.Entry(self.root,width=35, borderwidth=5)
        username_entry.grid(row=0, column=1, columnspan=1, padx=10, pady=10)
        password_label = tkinter.Label(self.root, width=35, borderwidth=5,text="password")
        password_label.grid(row=1, column=0, columnspan=1, padx=10, pady=10)
        password_entry  = tkinter.Entry(self.root,width=35, borderwidth=5)
        password_entry.grid(row=1, column=1, columnspan=1, padx=10, pady=10)
        setup_button = tkinter.Button(self.root,widt = 35, borderwidth= 5 , text="setup",command=lambda: self.sign_up(username_entry,password_entry))
        setup_button.grid(row = 2, column=0, columnspan=1, padx=10, pady=10)
    def sign_up(self,username_entry:tkinter.Entry,password_entry:tkinter.Entry):
        print("sign up")
        error_label = tkinter.Label(self.root, width=35, borderwidth=5)
        if username_entry.get() is not '':
            if password_entry.get() is not '':
                if re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$').match(password_entry.get()):
                    if self.sql_client.get_data_from_table(table_name='users',where = "where username=?",variables= (username_entry.get(),),amount_to_fetch=1,data_to_select="password") is None:
                        self.sql_client.add_user(username_entry.get(),password_entry.get())
                    else:
                        error_label.configure(text = "username already in usage")
                else:
                    error_label.config(width=100)
                    error_label.configure(text= "password has to be more than 8 characters and have at list one digit,one lowercase letter, one uppercase letter and one symbol")
            else:
                error_label.configure(text= "no password")
        else:
            error_label.configure(text = "no username")
        if error_label['text']!= "":
            error_label.grid(row = 2,column =1,columnspan=10, padx=10, pady=10)