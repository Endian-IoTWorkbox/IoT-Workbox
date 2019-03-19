#!/usr/bin/python3

from helpers.colours import plus, minus, warning, info
import re
import os
from modules.module import Module


class Privacy(Module):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_file = args[0]
        
        self.info = {
            'Name': 'Privacy Checker',
            'Author': 'Jolan Cupitt',
            'Description': 'Searches the file/data '
                           'for any forms of data deemed to be considered private and displays it to the user',
            }

        self.options = {
            'FilePath': {
                'Description': 'The file path is the path to the file that is going to be analysed',
                'Required': False, 
                'Value': ''
                },
            'DirectoryPath': {
                'Description': 'The directory path is the path to the directory that is going to be analysed',
                'Required': False,
                'Value': ''
            }
            
        }


    def validate_options(self):
        # Validate the options

        for key, value in self.options.items():
            if value['Required'] and value['Value'] == "":
                minus("Please fill in all required options")
                return False

        if self.options["FilePath"]["Value"] != "" :
            if not os.path.exists(self.options["FilePath"]["Value"]):
                minus("The path does not exist")
                return False

        if self.options["FilePath"]["Value"] == "" and self.options["DirectoryPath"]["Value"] == "":
            minus("Please either insert a file path or a directory path")
            return False

        return True
    
    def run(self):
    
        if not self.validate_options():
            return

        all_regex = {
            "Visa": r"\b([4]\d{3}[\s]\d{4}[\s]\d{4}[\s]\d{4}|[4]\d{3}[-]\d{4}[-]\d{4}[-]\d{4}|[4]\d{3}[.]\d{4}[.]\d{4}[.]\d{4}|[4]\d{3}\d{4}\d{4}\d{4})\b,",
            "Mastercard": r"^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$",
            "American Express": r"^3[47][0-9]{13}$",
            "American Date Format": r"^([1][12]|[0]?[1-9])[\/-]([3][01]|[12]\d|[0]?[1-9])[\/-](\d{4}|\d{2})$",
            "Uk Date Format": r"(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})",
            "Email Address": r"^[\w\.=-]+@[\w\.-]+\.[\w]{2,3}$",
            "IPV4 Address": r"^\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}$",
            "US Zip Code": r"^((\d{5}-\d{4})|(\d{5})|([A-Z]\d[A-Z]\s\d[A-Z]\d))$",
            "Uk Post Code": r"^(GIR 0AA)|[a-z-[qvx]](?:\d|\d{2}|[a-z-[qvx]]\d|[a-z-[qvx]]\d[a-z-[qvx]]|[a-z-[qvx]]\d{2})(?:\s?\d[a-z-[qvx]]{2})?$",
            "SSN": r"\b(?!000|666|9\d{2})([0-8]\d{2}|7([0-6]\d))([-]?|\s{1})(?!00)\d\d\2(?!0000)\d{4}\b",
        }

        if self.options["DirectoryPath"]["Value"]:

            all_files = os.listdir(self.options["DirectoryPath"]["Value"])
            for f in all_files:
                if self.options["DirectoryPath"]["Value"].endswith("/"):
                    filename = self.options["DirectoryPath"]["Value"] + f
                else:
                    filename = self.options["DirectoryPath"]["Value"] + "/" + f
                with open(filename,"r") as test:
                    data = test.read().splitlines()

                info("Parsing " + filename)
                self.log_to_file("Parsing " + filename)
                for line in data:
                    splitted = line.split(" ")
                    for word in splitted:
                        for key, value in all_regex.items():
                            tmp = re.findall(value, word)
                            if tmp:
                                print(key + "--> ", tmp)
                            
                                self.log_to_file("Results for " + key)
                                for t in tmp:
                                    if type(t) == tuple:
                                        for tup in t:
                                            self.log_to_file(tup)
                                    else:
                                        self.log_to_file(t)
        else:
            with open(self.options["FilePath"]["Value"], "r") as test:
                data = test.read().splitlines()
            
            info("Parsing " + self.options["FilePath"]["Value"])
            self.log_to_file("Parsing " + self.options["FilePath"]["Value"])

            for line in data:
                splitted = line.split(" ")
                for word in splitted:
                    for key, value in all_regex.items():
                        tmp = re.findall(value, word)
                        if tmp:
                            print(key + "--> ", tmp)
                            self.log_to_file("Results for " + key)
                            for t in tmp:
                                if type(t) == tuple:
                                    for tup in t:
                                        self.log_to_file(tup)
                                else:
                                    self.log_to_file(t)
