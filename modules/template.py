#!/usr/bin/python3

# Import what you need 
from helpers.colours import plus, minus, warning, info
from modules.module import Module
# To print information use either plus, minus, warning or info accordingly
# To test the module this should be added into the file in /core/cli.py
# Instruction to do that will be inside that file
# To run the program you need to run the file workbox.py



class ModuleName(Module):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
	self.log_file = args[0]

        self.info = {
            'Name': 'Name of the module',
            'Author': 'Your name',
            'Description': 'Description of what the module does',
            }

        self.options = {
            'Option 1': {
                'Description': 'Description of the option',
                'Required': True # or False,
                'Value': 'Value, leave blank or set a default'
                }

            # Add all options needed with the same format
        }


    def validate_options(self):
        # Validate the options

        for key, value in self.options.items():
            if value['Required'] and value['Value'] == "":
                minus("Please fill in all required options")
                return False

        # Check the options if they are correct
        # i.e IP address is a valid ip address
        # Port number is between 0 and 65535
        # etc.. 
        # Return False if it does not validate

        return True

    # This is the function where the module does its magic :) so all logic should be here
    def run(self):
        # if the options do not validate do not run the module
        if not self.validate_options():
            return
        # Logic of the module 

    # You are allowed to use as many methods as you want to make your module work, this should be called inside the run method
