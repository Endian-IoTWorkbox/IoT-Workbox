#!/usr/bin/python3

import re
import os
from helpers.colours import info, plus, minus, warning
import stat
import datetime
from modules.module import Module 


class LinuxRootFiles(Module):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.log_file = args[0]

        self.info = {
                'Name': 'Linux Root files',
                'Author': 'Alessandro Cara @ctrl_c3',
                'Description': 'Check if linux important files (/etc/passwd, /etc/shadow) are properly secured'
                }

        self.options = {
                'Verbose': {
                    'Description': 'Print verbose output',
                    'Required': False,
                    'Value': 'False'
                    }
                }

    def validate_options(self):
        
        for key, value in self.options.items():
            if value['Required'] == True and not value['Value']:
                minus("Please fill all required options")
                return False

        return True

    def run(self):
        error = 0

        if self.options['Verbose']['Value'] == "True":
            info("Checking file permissions for /etc/passwd")
            self.log_to_file("Checking file permissions for /etc/passwd")

        p = oct(stat.S_IMODE(os.stat('/etc/passwd').st_mode))[2:]
        info("/etc/passwd = %s" % p)
        self.log_to_file("/etc/passwd = " + p)
        
        if int(p) != 644:
            minus("/etc/passwd permissions should be 644 (-rw-r--r--)")
            self.log_to_file("/etc/passwd permissions shuld be 644 (-rw-r--r--)")
            error = 1 

        if self.options['Verbose']['Value'] == "True":
            info("Checking file permissions for /etc/shadow")
            self.log_to_file("Checking file permissions for /etc/shadow")
        
        s = oct(stat.S_IMODE(os.stat('/etc/shadow').st_mode))[2:]
        info("/etc/shadow = %s " % s)
        self.log_to_file("/etc/shadow = " + str(s))
        
        if int(s) != 640:
            minus("/etc/shadow permissions should be 640 (-rw-r-----)")
            self.log_to_file("/etc/shadow permissions shuold be 640 (-rw-r-----)")
            error = 1

        if self.options['Verbose']['Value'] == "True":
            info("Checking file permissions for /etc/group")
            self.log_to_file("Checking file permissions for /etc/group")

        g = oct(stat.S_IMODE(os.stat('/etc/group').st_mode))[2:]
        info("/etc/group = %s" % g)
        self.log_to_file("/etc/group = " + str(g))

        if int(g) != 644:
            minus("/etc/group permissions should be 640 (-rw-r--r--)")
            self.log_to_file("/etc/group permissions should be 640 (-rw-r--r--)")
            error = 1

        if error != 1:
            plus("Everything seems fine")
            self.log_to_file("Everything seems fine")
