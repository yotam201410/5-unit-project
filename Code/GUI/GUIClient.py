import re
import sqlite3
import tkinter
from HostFileManagment.HostManagment import HostClient
from SQLManagment.SQLClient import SQLClient
from typing import List
from NetworkTalk.MultiSocket import MultiSocket
from functools import partial
from tkinter import ttk


class GUIClient(object):
    buttons: List[ttk.Button]
    labels: List[ttk.Label]
    host_client: HostClient
    sql_client: SQLClient
    multi_socket: MultiSocket

    def __init__(self, sql_client: SQLClient, multi_socket: MultiSocket, host_client: HostClient):
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
        username_label = ttk.Label(self.root, width=35, text="Username")
        username_label.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        username_entry = ttk.Entry(self.root, width=35)
        username_entry.grid(row=0, column=1, columnspan=1, padx=10, pady=10)
        password_label = ttk.Label(self.root, width=35, text="Password")
        password_label.grid(row=1, column=0, columnspan=1, padx=10, pady=10)
        password_entry = ttk.Entry(self.root, width=35,show="*")
        password_entry.grid(row=1, column=1, columnspan=1, padx=10, pady=10)
        setup_button = ttk.Button(self.root, width=35, text="Setup",
                                      command=lambda: self.sign_up(username_entry, password_entry))
        setup_button.grid(row=2, column=0, columnspan=1, padx=10, pady=10)
        refresh_button = ttk.Button(self.root, width=35, text="Refresh",
                                        command=self.refresh_setup_page)
        refresh_button.grid(row=2, column=1, columnspan=1, padx=10, pady=10)
        self.elements += [username_label, username_entry, password_entry, setup_button, password_label, refresh_button]

    def sign_up(self, username_entry: ttk.Entry, password_entry: ttk.Entry):
        error_label = ttk.Label(self.root, width=35)
        self.elements.append(error_label)
        if username_entry.get() != '':
            if " " not in username_entry.get():
                if password_entry.get() != '':
                    if re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$').match(
                            password_entry.get()) and " " not in password_entry.get():
                        if self.sql_client.get_data_from_table(table_name='users', where="where username=?",
                                                               variables=(username_entry.get(),), amount_to_fetch=1,
                                                               data_to_select="password") is None:
                            username = username_entry.get()
                            self.sql_client.add_user(username_entry.get(), password_entry.get())
                            self.multi_socket.add_user(username_entry.get(), password_entry.get())
                            self.clear_page()
                            self.create_host_page(username)
                        else:
                            error_label.configure(text="Username already in usage")
                    else:
                        error_label.config(width=150)
                        error_label.configure(
                            text="Password has to be more than 8 characters and have at list one digit,one lowercase "
                                 "letter, one uppercase letter and one symbol with no space")
                else:
                    error_label.configure(text="No password")
            else:
                error_label.configure(text="Username has to contian no spaces")
        else:
            error_label.configure(text="No username")
        try:
            if error_label['text'] != '':
                error_label.grid(row=2, column=1, columnspan=10, padx=10, pady=10)
        except Exception:
            pass

    def create_login_page(self):
        username_label = ttk.Label(self.root, width=35, text="Username")
        username_label.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        username_entry = ttk.Entry(self.root, width=35)
        username_entry.grid(row=0, column=1, columnspan=1, padx=10, pady=10)
        password_label = ttk.Label(self.root, width=35, text="Password")
        password_label.grid(row=1, column=0, columnspan=1, padx=10, pady=10)
        password_entry = ttk.Entry(self.root, width=35,show="*")
        password_entry.grid(row=1, column=1, columnspan=1, padx=10, pady=10)
        login_button = ttk.Button(self.root, width=35, text="Login",
                                      command=lambda: self.login(username_entry, password_entry))
        login_button.grid(row=2, column=1, columnspan=1, padx=10, pady=10)
        refresh_button = ttk.Button(self.root, width=35, text="Refresh",
                                      command=self.refresh_setup_page)
        refresh_button.grid(row=2, column=0, columnspan=1, padx=10, pady=10)
        self.elements += [username_label, username_entry, password_entry, login_button, password_label,refresh_button]

    def login(self, username_entry: ttk.Entry, password_entry: ttk.Entry):
        user_data = self.sql_client.get_user(password_entry.get())
        if user_data is None or user_data[0] != username_entry.get():
            error_label = ttk.Label(self.root, width=35, text="Password or username doesnt match")
            error_label.grid(row=2, column=2, columnspan=10, padx=10, pady=10)
            self.elements.append(error_label)
        else:
            self.clear_page()
            self.create_host_page(user=user_data[0])

    def create_host_page(self, user: str):
        host_rows = self.sql_client.get_host_rows()
        row_counter = 0
        for domain_name in host_rows:
            domain_name = domain_name[0]
            label_domian = ttk.Label(self.root, width=35, text=domain_name)
            label_domian.grid(row=row_counter, column=0, columnspan=1, padx=10, pady=10)
            delete_button = ttk.Button(self.root, width=35, text="Delete",
                                           command=partial(self.delete_domain, domain_name, user))
            delete_button.grid(row=row_counter, column=1, columnspan=1, padx=10, pady=10)
            self.elements += [delete_button, label_domian]
            row_counter += 1
        domain_entry = ttk.Entry(self.root, width=35, text="Enter domain here")
        domain_entry.grid(row=row_counter, column=0, columnspan=1, padx=10, pady=10)
        add_domian_button = ttk.Button(self.root, width=35, text="Add domian",
                                           command=lambda: self.add_domain(domain_entry.get(), user))
        add_domian_button.grid(row=row_counter, column=1, columnspan=1, padx=10, pady=10)
        refresh_button = ttk.Button(self.root, width=35, text="Refresh",
                                        command=lambda: self.refresh_host_page(user))
        refresh_button.grid(row=row_counter + 1, column=0, columnspan=1, padx=10, pady=10)
        sync_button = ttk.Button(self.root, width=35, text="Sync", command=self.sync)
        sync_button.grid(row=row_counter + 1, column=1, columnspan=1, padx=10, pady=10)
        delete_user = ttk.Button(self.root, width=35,text="Delete user",
                                     command=lambda: self.delete_user_page(user))
        delete_user.grid(row=row_counter + 1, column=2, columnspan=1, padx=10, pady=10)
        self.elements += [add_domian_button, domain_entry, delete_user, sync_button, refresh_button]

    def sync(self):
        self.multi_socket.sync_data(self.sql_client)

    def refresh_host_page(self, user: str):
        self.clear_page()
        self.create_host_page(user)

    def delete_domain(self, domain_name, user):
        try:
            self.sql_client.delete_data_from_table("host", where="where domain=?", data=(domain_name,))
            self.host_client.remove_domain(domain_name)
            self.multi_socket.remove_domain(domain_name)
            self.clear_page()
            self.create_host_page(user)
        except Exception as e:
            raise e

    def add_domain(self, domain_name: str, user: str):
        try:
            self.sql_client.add_data_to_table("host", rows_to_set=("domain",), data=(domain_name,))
            self.host_client.add_domain(domain_name)
            self.multi_socket.add_domain(domain_name)
            self.clear_page()
            self.create_host_page(user)
        except sqlite3.IntegrityError:
            pass
        except Exception as e:
            raise e

    def delete_user_page(self, user: str):
        self.clear_page()
        password_label = ttk.Label(self.root, width=35, text=f"Enter the password of user: {user}")
        password_label.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        password_entry = ttk.Entry(self.root, width=35,show="*")
        password_entry.grid(row=0, column=1, columnspan=1, padx=10, pady=10)
        delete_button = ttk.Button(self.root, width=35, text="DELETE",
                                       command=lambda: self.delete_user(user, password_entry.get()))
        delete_button.grid(row=1, column=0, columnspan=1, padx=10, pady=10)
        self.elements += [password_label, password_entry, delete_button]

    def delete_user(self, user, password: str):
        if self.sql_client.get_user(password) is not None and self.sql_client.get_user(password)[0] == user:
            self.sql_client.delete_user(user)
            self.multi_socket.remove_user(user)
            self.clear_page()
            if len(self.sql_client.get_all_users()) == 0:
                self.create_sign_up_page()
            else:
                self.create_login_page()
        else:
            error_label = ttk.Label(self.root, width=35, text="Password doesnt match")
            error_label.grid(row=1, column=1, columnspan=10, padx=10, pady=10)
            self.elements.append(error_label)

    def refresh_setup_page(self):
        self.clear_page()
        if len(self.sql_client.get_all_users()) == 0:
            self.create_sign_up_page()
        else:
            self.create_login_page()
