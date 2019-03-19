#!/usr/bin/python3

header = '\033[95m'
blue = '\033[94m'
green = '\033[92m'
warn = '\033[93m'
fail = '\033[91m'
reset = '\033[0m'


def plus(to_print):
    print(blue + '[+] ' + reset + to_print)

def minus(to_print):
    print(fail + '[-] ' + reset + to_print)

def warning(to_print):
    print(warn + '[!] ' + reset + to_print)

def info(to_print):
    print(green + '[i] ' + reset + to_print)
