#!/usr/bin/python3

import sys
import os
from helpers.colours import plus, minus, warning, info
from tabulate import tabulate
from modules.portscan import PortScan
from modules.sshbruteforce import SSHBruteforce
from modules.ftpbruteforce import FTPBruteforce
from modules.userenum import UserEnumeration
from modules.sshdconfig import SSHDConfig
from modules.linuxrootfiles import LinuxRootFiles
from modules.privacyconcerns import PrivacyConcerns
# Need to import your module in here


class Cli(object):
    
    def __init__(self, context):
        self.prompt = "\n\033[95miotworkbox#>\033[0m "
        self.context = context
        self.activeModule = None
        
        # Add your module name and main class in this dictionary e.g "sqlinjection": SQLInjection()
        self.modules = {
                "Web interface": {
                    "userenum": UserEnumeration()
                    },
                "Authentication/Authorization": {
                    "linuxrootfiles": LinuxRootFiles(), 
                    "sshdconfig": SSHDConfig(), 
                    "sshbruteforce": SSHBruteforce(), 
                    "ftpbruteforce": FTPBruteforce()
                    },
                "Network": {
                    "portscan": PortScan()
                    },
                "Privacy": {
                    "privacyconcerns": PrivacyConcerns()
                    },
                "Transport Encryption": {
                    }
                }

    def run(self):
        while True:
            command = input(self.prompt)
            command_list = command.split(" ")

            if self.context == "main":
                if command_list[0] == "use":
                    for key, value in self.modules.items():
                        if command_list[1] in value.keys():
                            self.activeModule = value[command_list[1]]
                            self.prompt = "\n\033[95miotworkbox/modules#>\033[0m "
                            self.context = "modules"
                    if not self.activeModule:
                        minus(command_list[1] + " is not a valid module")

                elif command_list[0] == "help" or command_list[0] == "?":
                    self.main_help()

                elif command_list[0] == "list":
                    table = []
                    if len(command_list) == 2:
                        if command_list[1] == "all":
                            for key, value in self.modules.items():
                                for k, v in value.items():
                                    table.append([k])
                            print(tabulate(table, headers=["Modules"], tablefmt="grid"))
                        elif command_list[1] == "categories":
                            for key, value in self.modules.items():
                                table.append([key])
                            print(tabulate(table, headers=["Category"], tablefmt="grid"))
                        else:
                            minus("Please select a valid option, either list all or list categories")
                    else:
                        minus("Please select a valid option, either list all or list categories")

                elif command_list[0] == "clear":
                    os.system(command_list[0])

                elif command_list[0] == "exit" or command_list[0] == "quit":
                    info("Exiting..")
                    sys.exit(0)

                else:
                    info("Please select a valid option")
                
            elif self.context == "modules":
                if command_list[0] == "set":
                    if len(command_list) != 3:
                        warning("Please type a valid command")
                    else:
                        try:
                            self.activeModule.options[command_list[1]]['Value'] = command_list[2]
                            info("Option %s set to %s" % (command_list[1], command_list[2]))
                        except Exception:
                            minus("Failed to add option %s" % command_list[1])
                
                elif command_list[0] == "back" or command_list[0] == "main":
                    self.prompt = "\n\033[95miotworkbox#>\033[0m "
                    self.context = "main"
                
                elif command_list[0] == "help" or command_list[0] == "?":
                    self.modules_help()

                elif command_list[0] == "run":
                    if self.activeModule.validate_options():
                        self.activeModule.run()

                elif command_list[0] == "options":
                    self.activeModule.print_options()

                elif command_list[0] == "info":
                    self.activeModule.print_info()

                elif command_list[0] == "clear":
                    os.system(command_list[0])
                
                elif command_list[0] == "exit" or command_list[0] == "quit":
                    info("Exiting..")
                    sys.exit(0)
                
                else:
                    info("Please select a valid option")

    def modules_help(self):
        table = [["?", "Display this menu"], ["help", "Display this menu"],
                 ["exit", "exit from the program"], ["options", "Print module's options"],
                 ["info", "Print module's info"]]

        print(tabulate(table, headers=["Command", "Description"], tablefmt="grid"))

    def main_help(self):
        table = [["?", "Display this menu"], ["help", "Display this menu"],
                 ["use", "use a module"], ["exit", "exit from the program"],
                 ["list all", "list all modules"], ["list categories", "list modules categories"]]

        print(tabulate(table, headers=["Command", "Description"], tablefmt="grid"))
