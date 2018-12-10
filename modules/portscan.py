from helpers.colours import plus, minus, warning, info
import os
from tabulate import  tabulate


class PortScan(object):

    def __init__(self):

        self.info = {
            'Name': 'Port scan',

            'Author': 'Alessandro Cara',

            'Description': 'Scans the host for open ports'
        }

        self.options = {
            'Ports': {
                'Description': 'Port range to scan',
                'Required': False,
                'Value': ''
            },
            'Ip': {
                'Description': 'Ip to scan',
                'Required': True,
                'Value': ''
            },
            'ScanMode': {
                'Description': 'Scan mode, UDP or TCP',
                'Required': True,
                'Value': 'TCP'
            },
            'ServiceEnumeration': {
                'Description': 'Enumerate services',
                'Required': False,
                'Value': False
            }
        }

    def validate_options(self):

        for option in self.options:
            if self.options[option]['Required'] and not self.options[option]['Value']:
                minus(option + ' is required ')
                return False
        if self.options['ServiceEnumeration']['Value']:
            if self.options['ServiceEnumeration']['Value'] != True and self.options['ServiceEnumeration'][
                                                                                     'Value'] != False:
                warning("Please set ServiceEnumeration to either True or False")
                return False

            else:
                self.options['ServiceEnumeration']['Value'] = '-sC -sV'

        if self.options['Ports']['Value']:
            if '-' in self.options['Ports']['Value']:
                try:
                    port1 = self.options['Ports']['Value'].split("-")[0]
                    port2 = self.options['Ports']['Value'].split("-")[1]
                    if int(port1) > 65535 and int(port1) < 0 or int(port2) > 65535 and int(port2) < 0:
                        warning("Port numbers go from 0 to 65535")
                        return False
                except Exception:
                    warning("Please insert a valid port or port range, i.e 0-65535")
                    return False
            else:
                try:
                    if int(self.options['Ports']['Value']) > 65535 and int(self.options['Ports']['Value'] < 0):
                        warning("Port numbers go from 0 to 65535")
                        return False
                except Exception:
                    warning("Please insert a valid port or port range, i.e 0-65535")
                    return False

        if self.options['ScanMode']['Value'].lower() != 'tcp' and self.options['ScanMode']['Value'].lower() != 'udp':
            warning("Please select either TCP or UDP")
            return False
        return True

    def run(self):
        if not self.validate_options():
            return
        command = "nmap %s %s %s %s" % ('-sU' if 'udp' in self.options['ScanMode']['Value'].lower()
                                        else '-sT', '-p ' + self.options['Ports']['Value']
                                        if self.options['Ports']['Value'] else '', '-sC -sV'
                                        if self.options['ServiceEnumeration']['Value'] == 'True' else '',
                                        self.options['Ip']['Value'])
        try:
            info("Result for port scan module on %s" % self.options["Ip"]["Value"])
            os.system(command)

        except Exception:
            minus("Module failed to run")

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
