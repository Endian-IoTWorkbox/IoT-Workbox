#!/usr/bin/python3

from helpers.colours import plus, minus, warning, info
import os
import requests
from modules.module import Module


class SQLInjection(Module):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_file = args[0]

        self.info = {
            'Name': 'SQL Injection',
            'Author': 'Alessandro Cara',
            'Description': 'This module checks for SQL Injection vulnerabilities',
            }

        self.options = {
            'URL': {
                'Description': 'Target URL',
                'Required': True,
                'Value': ''
                },
            'Wordlist': {
                'Description': 'Path to the payloads wordlist',
                'Required': True,
                'Value': ''
                },
            'Parameter': {
                'Description': 'Parameter to test for SQLi',
                'Required': True,
                'Value': ''
                },
            'Method': {
                'Description': 'HTTP Method, GET or POST',
                'Required': True,
                'Value': ''
                },
            'Verbose': {
                'Description': 'Be verbose with output',
                'Required': False,
                'Value': False
                }
        }


    def validate_options(self):
        # Validate the options

        for key, value in self.options.items():
            if value['Required'] and value['Value'] == "":
                minus("Please fill in all required options")
                return False

        if not os.path.exists(self.options['Wordlist']['Value']):
            minus("The wordlist does not exists")
            return False

        if self.options["Method"]["Value"].lower() != "post" and self.options["Method"]["Value"].lower() != "get":
            minus("Method can either be GET or POST")
            return False
        return True
    
    def run(self):
        # if the options do not validate do not run the module
        if not self.validate_options():
            return
        
        with open(self.options['Wordlist']['Value'], 'r') as wordlist:
            wd = wordlist.read().splitlines()
        
        for payload in wd:
            if self.options["Method"]["Value"].lower() == "post":
                data = {self.options["Parameter"]["Value"]: payload}
                try:
                    resp = requests.post(self.options["URL"]["Value"], data)
                    if self.options["Verbose"]["Value"]:
                        info(resp.text)
                    if "error" in resp.text:
                        info("Possible SQLInjection was found, payload = " + payload)
                        self.log_to_file("Possible SQLInjection was found, payload = " + payload)
                    elif resp.status_code == 500:
                        info("Server returned code 500")
                        self.log_to_file("Server returned code 500")
                except Exception:
                    info("Error processing the request")
            else:
                try:
                    resp = requests.get(self.options["URL"]["Value"] + "?" + self.options["Parameter"]["Value"] + "=" + payload)
                    if self.options["Verbose"]["Value"]:
                        info(resp.text)
                    if "error" in resp.text:
                        info("Possible SQLInjection was found, payload = " + payload)
                        self.log_to_file("Possible SQLInjection was found, payload = " + payload)
                    elif resp.status_code == 500:
                        info("Server returned code 500")
                        self.log_to_file("Server returned code 500")
                except Exception:
                    info("Error processing the request")
