#!/usr/bin/python3

from helpers.colours import plus, minus, warning, info
import sys
try:
    from tabulate import tabulate
except ImportError:
    minus("Make sure all required modules are installed")
    sys.exit(0)
import datetime


class Module(object):

    def __init__(self, *args, **kwargs):
        
        self.log_file = args[0]

        self.info = {
            }

        self.options = {
                }



    def validate_options(self):
        # Validate the options

        for key, value in self.options.items():
            if value['Required'] and value['Value'] == "":
                minus("Please fill in all required options")
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

    # Log to file 
    def log_to_file(self, content):
        with open(self.log_file, "a+") as log:
            log.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "  " + content + "\n")

    # This is the function where the module does its magic :) so all logic should be here
    def run(self):
        # if the options do not validate do not run the module
        if not self.validate_options():
            return


        

