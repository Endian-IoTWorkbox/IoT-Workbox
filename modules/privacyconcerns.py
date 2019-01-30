#!/usr/bin/python3

from helpers.colours import plus, minus, warning, info
from tabulate import tabulate
import re
import os


class PrivacyConcerns(object):

    def __init__(self, *args, **kwargs):
        
        # All regexs
        self.regexs = {
                "Email": r"^[\w\.=-]+@[\w\.-]+\.[\w]{2,3}$",
                "Social security number": r"\b(?!000|666|9\d{2})([0-8]\d{2}|7([0-6]\d))([-]?|\s{1})(?!00)\d\d\2(?!0000)\d{4}\b",
                "Ipv4 address": r"^\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}$",
                "Mastercard": r"^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$",
                "Visa": r"b([4]\d{3}[\s]\d{4}[\s]\d{4}[\s]\d{4}|[4]\d{3}[-]\d{4}[-]\d{4}[-]\d{4}|[4]\d{3}[.]\d{4}[.]\d{4}[.]\d{4}|[4]\d{3}\d{4}\d{4}\d{4})\b",
                "American express": r"^3[47][0-9]{13}$",
                "US Zip code": r"^((\d{5}-\d{4})|(\d{5})|([A-Z]\d[A-Z]\s\d[A-Z]\d))$",
                "File path": r"\\[^\\]+$",
                "Url": r"(?i)\b((?:[a-z][\w-]+:(?:\/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}\/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
                }

        self.info = {
            'Name': 'Privacy Concerns',
            'Author': 'Alessandro Cara',
            'Description': 'This module checks file for sensible information, e.g c/c numbers, ip addresses etc',
            }

        self.options = {
            'FilePath': {
                'Description': 'Path to the file to be checked',
                'Required': True,
                'Value': ''
                },
            }


    def validate_options(self):
        # Validate the options

        for key, value in self.options.items():
            if value['Required'] and value['Value'] == "":
                minus("Please fill in all required options")
                return False
        if not os.path.exists(self.options["FilePath"]["Value"]):
            minus("The path to the file is not valid")
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

        # Open file
        with open(self.options["FilePath"]["Value"], "r") as suspectFile:
            data = suspectFile.read().splitlines()

        results = {}
        # Set results value to be empty lists
        for key, value in self.regexs.items():
            results[key] = []

        for line in data:
            words = line.split(" ")
            for word in words:
            
                for key, value in self.regexs.items():
                    
                    tmp = re.findall(value, word)
                    if tmp:
                        results[key].append(tmp)
            
        info("Results: ")
        for key, value in results.items():
            for item in value:
                for x in item:
                    print(key, " --> " , x)
