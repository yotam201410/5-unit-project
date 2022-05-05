import re
import sqlite3
import tkinter
from HostFileManagment.HostManagment import HostClient
from SQLManagment.SQLClient import SQLClient
from typing import List
from NetworkTalk.MultiSocket import MultiSocket


class GUIClient(object):
    buttons: List[tkinter.Button]
    labels: List[tkinter.Label]

    def __init__(self, sql_client: SQLClient, multi_socket: MultiSocket,host_client: HostClient):
        self.host_client = host_client
        self.sql_client = sql_client
        self.multi_socket = multi_socket
        self.root = tkinter.Tk(screenName="Guard Client")
        self.root.title("Guard Client")
        self.elements = []
        self.host_elements = {}
        if len(self.sql_client.get_all_users()) == 0:
            self.create_sign_up_page()
        else:
            self.create_login_page()
        print("GUI Is Up")
        self.main_loop()

    def clear_page(self):
        for i in self.elements:
            i.destroy()

    def main_loop(self):
        self.root.mainloop()

    def create_sign_up_page(self):
        username_label = tkinter.Label(self.root, width=35, borderwidth=5, text="Username")
        username_label.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        username_entry = tkinter.Entry(self.root, width=35, borderwidth=5)
        username_entry.grid(row=0, column=1, columnspan=1, padx=10, pady=10)
        password_label = tkinter.Label(self.root, width=35, borderwidth=5, text="Password")
        password_label.grid(row=1, column=0, columnspan=1, padx=10, pady=10)
        password_entry = tkinter.Entry(self.root, width=35, borderwidth=5)
        password_entry.grid(row=1, column=1, columnspan=1, padx=10, pady=10)
        setup_button = tkinter.Button(self.root, width=35, borderwidth=5, text="Setup",
                                      command=lambda: self.sign_up(username_entry, password_entry))
        setup_button.grid(row=2, column=0, columnspan=1, padx=10, pady=10)
        self.elements += [username_label, username_entry, password_entry, setup_button, password_label]

    def sign_up(self, username_entry: tkinter.Entry, password_entry: tkinter.Entry):
        error_label = tkinter.Label(self.root, width=35, borderwidth=5)
        self.elements.append(error_label)
        if username_entry.get() != '':
            if password_entry.get() != '':
                if re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$').match(
                        password_entry.get()):
                    if self.sql_client.get_data_from_table(table_name='users', where="where username=?",
                                                           variables=(username_entry.get(),), amount_to_fetch=1,
                                                           data_to_select="password") is None:
                        username = username_entry.get()
                        self.sql_client.add_user(username_entry.get(), password_entry.get())
                        self.clear_page()
                        self.create_host_page(username)
                    else:
                        error_label.configure(text="Username already in usage")
                else:
                    error_label.config(width=100)
                    error_label.configure(
                        text="Password has to be more than 8 characters and have at list one digit,one lowercase "
                             "letter, one uppercase letter and one symbol")
            else:
                error_label.configure(text="No password")
        else:
            error_label.configure(text="No username")
        try:
            if error_label['text'] != '':
                error_label.grid(row=2, column=1, columnspan=10, padx=10, pady=10)
        except Exception:
            pass

    def create_login_page(self):
        username_label = tkinter.Label(self.root, width=35, borderwidth=5, text="Username")
        username_label.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        username_entry = tkinter.Entry(self.root, width=35, borderwidth=5)
        username_entry.grid(row=0, column=1, columnspan=1, padx=10, pady=10)
        password_label = tkinter.Label(self.root, width=35, borderwidth=5, text="Password")
        password_label.grid(row=1, column=0, columnspan=1, padx=10, pady=10)
        password_entry = tkinter.Entry(self.root, width=35, borderwidth=5)
        password_entry.grid(row=1, column=1, columnspan=1, padx=10, pady=10)
        login_button = tkinter.Button(self.root, width=35, borderwidth=5, text="Login",
                                      command=lambda: self.login(username_entry, password_entry))
        login_button.grid(row=2, column=0, columnspan=1, padx=10, pady=10)
        self.elements += [username_label, username_entry, password_entry, login_button, password_label]

    def login(self, username_entry: tkinter.Entry, password_entry: tkinter.Entry):
        user_data = self.sql_client.get_user(password_entry.get())
        if user_data is None or user_data[0] != username_entry.get():
            error_label = tkinter.Label(self.root, width=35, borderwidth=5, text="Password or username doesnt match")
            error_label.grid(row=2, column=1, columnspan=10, padx=10, pady=10)
            self.elements.append(error_label)
        else:
            self.clear_page()
            self.create_host_page(user=user_data[0])

    def create_host_page(self, user: str):
        host_rows = self.sql_client.get_host_rows()
        row_counter = 0
        for domain_name in host_rows:
            domain_name = domain_name[0]
            label_domian = tkinter.Label(self.root, width=35, borderwidth=5, text=domain_name)
            label_domian.grid(row=row_counter, column=0, columnspan=1, padx=10, pady=10)
            delete_button = tkinter.Button(self.root, width=35, borderwidth=5, text="Delete",
                                           command=lambda: self.delete_domain(domain_name, user))
            delete_button.grid(row=row_counter, column=1, columnspan=1, padx=10, pady=10)
            self.elements += [delete_button, label_domian]
            row_counter += 1
        domain_entry = tkinter.Entry(self.root, width=35, borderwidth=5, text="enter domain here")
        domain_entry.grid(row=row_counter, column=0, columnspan=1, padx=10, pady=10)
        add_domian_button = tkinter.Button(self.root, width=35, borderwidth=5, text="Add domian",
                                           command=lambda: self.add_domain(domain_entry.get(), user))
        add_domian_button.grid(row=row_counter, column=1, columnspan=1, padx=10, pady=10)
        delete_user = tkinter.Button(self.root, width=35, borderwidth=5, text="delete user",
                                     command=lambda: self.delete_user_page(user))
        delete_user.grid(row=row_counter + 1, column=2, columnspan=1, padx=10, pady=10)
        self.elements += [add_domian_button, domain_entry, delete_user]

    def delete_domain(self, domain_name, user):
        try:
            self.sql_client.delete_data_from_table("host", where="where domain=?", data=(domain_name,))
            self.host_client.remove_domain(domain_name)
            self.clear_page()
            self.create_host_page(user)
        except Exception as e:
            raise e

    def add_domain(self, domain_name: str, user: str):
        try:
            self.sql_client.add_data_to_table("host", rows_to_set=("domain",), data=(domain_name,))
            self.host_client.add_domain(domain_name)
            self.clear_page()
            self.create_host_page(user)
        except sqlite3.IntegrityError:
            pass
        except Exception as e:
            raise e

    def delete_user_page(self, user: str):
        self.clear_page()
        password_label = tkinter.Label(self.root, width=35, borderwidth=5, text=f"enter the password of user: {user}")
        password_label.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        password_entry = tkinter.Entry(self.root, width=35, borderwidth=5)
        password_entry.grid(row=0, column=1, columnspan=1, padx=10, pady=10)
        delete_button = tkinter.Button(self.root, width=35, borderwidth=5, text="DELETE",
                                       command=lambda: self.delete_user(user, password_entry.get()))
        delete_button.grid(row=1, column=0, columnspan=1, padx=10, pady=10)
        self.elements += [password_label, password_entry, delete_button]

    def delete_user(self, user, password: str):
        if self.sql_client.get_user(password) is not None and self.sql_client.get_user(password)[0] == user:
            self.sql_client.delete_user(user)
            self.clear_page()
            if len(self.sql_client.get_all_users()) == 0:
                self.create_sign_up_page()
            else:
                self.create_login_page()
        else:
            error_label = tkinter.Label(self.root, width=35, borderwidth=5, text="Password doesnt match")
            error_label.grid(row=1, column=1, columnspan=10, padx=10, pady=10)
            self.elements.append(error_label)
