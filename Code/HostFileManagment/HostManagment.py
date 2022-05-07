import ctypes
import sys
import threading
from typing import *


class HostClient:
    def __init__(self):
        self.deafult_host_file = """# Copyright (c) 1993-2009 Microsoft Corp.
#
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
#
# This file contains the mappings of IP addresses to host names. Each
# entry should be kept on an individual line. The IP address should
# be placed in the first column followed by the corresponding host name.
# The IP address and the host name should be separated by at least one
# space.
#
# Additionally, comments (such as these) may be inserted on individual
# lines or following the machine name denoted by a '#' symbol.
#
# For example:
#
#      102.54.94.97     rhino.acme.com          # source server
#       38.25.63.10     x.acme.com              # x client host

# localhost name resolution is handle within DNS itself.
#       127.0.0.1       localhost
#       ::1             localhost"""
        self.lock = threading.Lock()

    def remove_enter(self, lines: List[str]) -> List[str]:
        for line_index in range(len(lines)):
            if lines[line_index].endswith("\n"):
                lines[line_index] = lines[line_index][0:-1]
        return lines

    def get_readlines_from_read(self,text:str):
        text =text.split('\n')
        return [z+"\n" for z in text]
    def domain_in_file(self, file_lines, domain):
        lines = self.remove_enter(file_lines)
        for line in lines:
            splitted_line = line.split(" ")
            if len(splitted_line) == 2:
                if splitted_line[1] == domain:
                    return True
        return False

    def add_domain(self, domain: str):
        self.lock.acquire()
        read_file = self.open_read_file()
        read_text = read_file.read()
        read_lines = self.get_readlines_from_read(read_text)
        if not self.domain_in_file(read_lines, domain):
            write_file = self.open_write_file()
            write_file.write(read_text + "\n127.0.0.1 " + domain + "\n127.0.0.1 www." + domain)
            write_file.close()
        read_file.close()
        self.lock.release()

    def remove_domain(self, domain):
        self.lock.acquire()
        read_file = self.open_read_file()
        read_lines = read_file.readlines()
        write_text = ""
        if self.domain_in_file(read_lines, domain):
            lines_without_enter = self.remove_enter(read_lines)
            for line in lines_without_enter:
                if not f"127.0.0.1 {domain}"==line and not f"127.0.0.1 www.{domain}" == line:
                    write_text +=line+"\n"
            write_file = self.open_write_file()
            write_file.write(write_text[0:-1])
            write_file.close()
        read_file.close()
        self.lock.release()

    def return_to_defult(self):
        self.lock.acquire()
        write_file = self.open_write_file()
        write_file.write(self.deafult_host_file)
        write_file.close()
        self.lock.release()

    def open_write_file(self):
        file = open("C:\Windows\System32\drivers\etc\hosts", 'w')
        return file

    def open_read_file(self):
        file = open("C:\Windows\System32\drivers\etc\hosts", 'r')
        return file


if __name__ == '__main__':
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False


    if is_admin():
        c = HostClient()
        # c.return_to_defult()
        c.add_domain("yotam.com")
        c.remove_domain("yotam.com")
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
