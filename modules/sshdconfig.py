#!/usr/bin/python3

from helpers.colours import plus, minus, warning, info
from tabulate import tabulate
import os
import ipaddress
import re
from modules.module import Module


class SSHDConfig(Module):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.log_file = args[0]

        self.info = {

            'Name': 'SSHD Config',
            'Author': ' Alessandro Cara',
            'Description': 'Check the sshd config file for misconfigurations'
            }
        
        self.options = {

            'Path': {
                'Description': 'Path to the sshd config file',
                'Required': True,
                'Value': '/etc/ssh/sshd_config'
                },
            
	    'Verbose': {
                'Description': 'Print all attempts',
                'Required': False,
                'Value': "False"
                }
            }

    def validate_options(self):

        for key, value in self.options.items():
            if value['Required'] and value['Value'] == "":
                minus("Please fill all required options")
                return False
        
        if not os.path.exists(self.options['Path']['Value']):
            minus("The file does not exists")
            return False
        return True

    def run(self):
        
        with open(self.options['Path']['Value'], "r") as sshd:
            content = sshd.read().splitlines()
       
        if self.options['Verbose']['Value'] == "True":
            info("Checking if X11Forwarding is enabled")
            self.log_to_file("Checking if X11Forwarding is enabled")

        if "X11Forwarding yes" in content:
            minus("X11 Forwarding is enabled, please disasble it unless is not necessary needed")
            self.log_to_file("X11 Forwarding is enabled, please disable it unless is not necessary needed")
        else:
            plus("X11Forwarding is disabled")
            self.log_to_file("X11Forwarding is disabled")

        if self.options['Verbose']['Value'] == "True":
            info("Checking if rhosts authentication method is enabled")
            self.log_to_file("Checking if rhosts authentication method is enabled")

        if "IgnoreRhosts no" in content:
            minus("Rhosts authentication is considered weak security, please disable it")
            self.log_to_file("Rhosts authentication is considered weak security, please disable it")
        else:
            plus("Rhosts authentication is disabled") 
            self.log_to_file("Rhosts authentication is disabled")

        if self.options['Verbose']['Value'] == "True":
            info("Checking if DNS hostname checking is enabled")
            self.log_to_file("Checking if DNS hostname checking is enabled")

        if "UseDNS no" in content or "#UseDNS no" in content:
            info("Consider using DNS hostname checking to enhance security controls")
            self.log_to_file("Consider using DNS hostname checking to enhance security controls")
        else:
            plus("DNS hostname checking is in use")
            self.log_to_file("DNS hostname checking is in use")

        if self.options['Verbose']['Value'] == "True":
            info("Checking if empty password authentication is enabled")
            self.log_to_file("Checking if empty password authentication is enabled")

        if "PermitEmptyPassword yes" in content:
            minus("Empty password authentication is enabled, please disable this for better security")
            self.log_to_file("Empty password authentication is enabled, please disable this for better security")
        else:
            plus("Empty password authentication is disabled")
            self.log_to_file("Empty password authentication is enabled")

        if self.options['Verbose']['Value'] == "True":
            info("Checking anti bruteforce lockout")
            self.log_to_file("Checking anti bruteforce lockout")
        for line in content:
            if "#MaxAuthTries " in line or "MaxAuthTries " in line:
                lockout_number = re.findall(r"\d", line)[0]
                if int(lockout_number) > 6:
                    info("Please consider allowing less authentication attempts to prevent account bruteforce attacks")
                    self.log_to_file("Please consider allowing less authentication attempts to prevent account bruteforce attacks")
                    break
                elif int(lockout_number) <= 6:
                    plus("The account lockout mechanism is secure enough, although try and keep this at a minimun")
                    self.log_to_file("The accout lockout mechanism is secure, although try and keep this at a minimun")
                    break
        if not lockout_number:
            minus("No account lockout option was found, consider using a lockout mechanism")
            self.log_to_file("No account lockout option was found, consider using a lockout mechanism")

        if self.options['Verbose']['Value'] == "True":
            info("Checking if root login is enabled")
            self.log_to_file("Checking if root login is enabled")
        if "PermitRootLogin yes" in content:
            minus("Consider disabling root login, you can always use sudo :) ")
            self.log_to_file("Consider disabling root login, you can always use sudo :) ")
        else:
            plus("Root login is disabled")
            self.log_to_file("Root login is disabled")

        if self.options['Verbose']['Value'] == "True":
            info("Checking if password authentication is disasbled and public key authentication is enabled")
            self.log_to_file("Checking if password authentication is disabled and public key authentication is enabled")

        if "PasswordAuthentication yes " in content and "PubkeyAuthentication no" in content:
            info("Consider disabling password authentication and use public key auth instead")
            self.log_to_file("Consider disabling passwod authentication nad use public key auth instead")
        else:
            plus("Publickey authentication is in place instead of password authentication")
            self.log_to_file("Publickey authentication is in place instead of password authentication")

        if self.options['Verbose']['Value'] == "True":
            info("Checking if protocol 2 is in use")
            self.log_to_file("Checking if protocol 2 is in use")

        if "Protocol 1" in content:
            minus("Consider forcing ssh protocol 2 usage, it's much more secure")
            self.log_to_file("Consider forcing ssh protocol 2 usage, it's much more secure")
        else:
            plus("SSH Protocol 2 is in use")
            self.log_to_file("SSH Protocol 2 is in use")
