# IoT-Workbox

IoT-Workbox is framework which can be used to assess IoT devices security. 

# Install

To install, simply clone the repository, then install all required modules included in the "requirements.txt" file.

# Contributing

In order to contribute please submit a pull request with your new module to the dev branch.
Modules should extend the module.py base class and provide a unique functionality (i.e. check for sql injection; lfi/rfi etc.).
A template is provided inside the module directory, please fill this with your module functionality.
All module shuold implement a run method which contains the main logic for the module.
Finally, to test the module, it shuold be imported in the cli.py script, a key:value pair in the for of ("module name": className()) should be inserted into the modules dictionary.


