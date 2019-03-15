#!/usr/bin/python3

import sys
import os
import datetime
from helpers.colours import plus, minus, warning, info
from tabulate import tabulate
from modules.portscan import PortScan
from modules.sshbruteforce import SSHBruteforce
from modules.ftpbruteforce import FTPBruteforce
from modules.userenum import UserEnumeration
from modules.sshdconfig import SSHDConfig
from modules.linuxrootfiles import LinuxRootFiles
from modules.sqlinjection import SQLInjection
from modules.xss import XSS
from modules.privacy import Privacy
# Need to import your module in here


class Cli(object):
    
    def __init__(self, context, log_file_path):
        self.prompt = "\n\033[95miotworkbox#>\033[0m "
        self.context = context
        self.activeModule = None
        self.log_file_path = log_file_path
        
        # Add your module name and main class in this dictionary e.g "sqlinjection": SQLInjection()
        self.modules = {
                "WebInterface": {
                    "userenum": UserEnumeration(log_file_path),
                    "sqlinjection": SQLInjection(log_file_path),
                    "xss": XSS(log_file_path)
                    },
                "Authentication/Authorization": {
                    "linuxrootfiles": LinuxRootFiles(log_file_path), 
                    "sshdconfig": SSHDConfig(log_file_path), 
                    "sshbruteforce": SSHBruteforce(log_file_path), 
                    "ftpbruteforce": FTPBruteforce(log_file_path)
                    },
                "Network": {
                    "portscan": PortScan(log_file_path)
                    },
                "Privacy": {
                    "privacyconcerns": Privacy(log_file_path)
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
                        elif command_list[1] in self.modules.keys():
                            for module in self.modules[command_list[1]]:
                                table.append([module])
                            print(tabulate(table, headers=[command_list[1]], tablefmt="grid"))
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
                    try:
                        if self.activeModule.validate_options():
                            self.log_to_file("Starting " + self.activeModule.__class__.__name__)
                            self.log_to_file("Options: ")
                            for key, value in self.activeModule.options.items():
                                self.log_to_file(str(key) + " --> " + str(value["Value"]))
                            self.activeModule.run()
                    except KeyboardInterrupt:
                        pass
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
                 ["exit", "Exit from the program"], ["options", "Print module's options"],
                 ["info", "Print module's info"], ["set", "Set an option, e.g set FilePath test.txt"],
                 ["run", "Run the module"]]

        print(tabulate(table, headers=["Command", "Description"], tablefmt="grid"))

    def main_help(self):
        table = [["?", "Display this menu"], ["help", "Display this menu"],
                 ["use", "Use a module"], ["exit", "Exit from the program"],
                 ["list all", "List all modules"], ["list categories", "List modules categories"],
                 ["list (category name)", "List all modules for a particular category"]]

        print(tabulate(table, headers=["Command", "Description"], tablefmt="grid"))

    def log_to_file(self, content):
        with open(self.log_file_path, "a+") as log:
            log.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + content + "\n")
