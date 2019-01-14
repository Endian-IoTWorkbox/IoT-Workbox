#!/usr/bin/python3

from helpers.colours import plus, minus, warning, info
from tabulate import tabulate
from urllib.parse import urlparse
import requests
import os
import string
import secrets

class UserEnumeration(object):

    def __init__(self, *args, **kwargs):
        
        self.info = {
            'Name': 'Username Enumeration',
            'Author': 'Alessandro Cara',
            'Description': 'This module enumerates usernames from a website',
            }

        self.options = {
            'URI': {
                'Description': 'URI of the page to test',
                'Required': True ,
                'Value': ''
                },
            'Wordlist': {
                'Description': 'Path to the username wordlist',
                'Required': True,
                'Value': ''
                },
            'UsernameParameter': {
                'Description': 'Field name for the username',
                'Required': True,
                'Value': ''
                },
            'OtherParameters': {
                'Description': 'Other parameters to fill, comma separated',
                'Required': True,
                'Value': ''
                },
            'Verbose': {
                'Description': 'Be more verbose',
                'Required': False,
                'Value': 'False'
                }
            
        }


    def validate_options(self):
        # Validate the options

        for key, value in self.options.items():
            if value['Required'] and value['Value'] == "":
                minus("Please fill in all required options")
                return False

        if not urlparse(self.options['URI']['Value']):
            minus("Please insert a valid URI")
            return False
 
        if not os.path.exists(self.options['Wordlist']['Value']):
            minus("The wordlist file does not exists")
            return False

        return True

    def print_options(self):
        table = []
        for key, value in self.options.items():
            table.append([key, value['Description'], value['Value'], value['Required']])
        print(tabulate(table, headers=["Option", "Description", "Value", "Required"], tablefmt="grid"))

    def print_info(self):
        table = []
        for key, value in self.info.items():
            table.append([key, value])

        print(tabulate(table, headers=["Info", "Value"], tablefmt="grid"))


    def run(self):
        # if the options do not validate do not run the module
        if not self.validate_options():
            return
        
        # Get invalid username
        try:
            parameters = self.options["OtherParameters"]["Value"].split(",")
        except Exception:
            minus("Parameters should be comma separated, i.e name,email,password")
            return
        data = {}
        for parameter in parameters:
            data[parameter] = "test@email.com"
        data[self.options['UsernameParameter']['Value']] = "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + "@test.com"

        resp = requests.post(self.options["URI"]["Value"], data=data)
        result = resp.text
        
        if self.options['Verbose']['Value'] == "True":
            info("Parsing the wordlist %s" %self.options["Wordlist"]["Value"])
        with open(self.options["Wordlist"]["Value"], "rb") as inFile:
            wd = inFile.read().splitlines()

        for username in wd:
            if self.options["Verbose"]["Value"] == "True":
                info("Trying %s" %username)
            data[self.options["UsernameParameter"]["Value"]] = username
            resp = requests.post(self.options["URI"]["Value"], data=data)

            if ((resp.text == result) == False):
                plus("Found valid username %s" %username)
    
        
