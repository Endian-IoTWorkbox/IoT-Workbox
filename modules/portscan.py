#!/usr/bin/pyton3

from helpers.colours import plus, minus, warning, info
import os
import threading
import socket
import ipaddress
from modules.module import Module


class PortScan(Module):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_file = args[0]
        self.screen_lock = threading.Semaphore(value=1)

        self.info = {
            'Name': 'Port scan',
            'Author': 'Nantawat Coombs',
            'Description': 'Scans the host for open ports'
        }

        self.options = {
            'Ip': {
                'Description': 'Ip to scan',
                'Required': True,
                'Value': ''
            },
            'FirstPort': {
                'Description': 'First port to scan',
                'Required': False,
                'Value': ''
            },
            'LastPort': {
                'Description': 'Last port to scan',
                'Required': False,
                'Value': ''
            }
        }

    def validate_options(self):

        for option in self.options:
            if self.options[option]['Required'] and not self.options[option]['Value']:
                minus(option + ' is required ')
                return False

        if not self.options['FirstPort']['Value'] and not self.options['LastPort']['Value']:
                minus("Please insert a port range to scan")
                return False

        if self.options['FirstPort']['Value']:
            try:
                if int(self.options['FirstPort']['Value']) > 65535 and int(self.options['FirstPort']['Value'] < 0):
                    minus("Ports cannot be < than 0 or > than 65535")
                    return False
            except Exception:
                minus("Please insert a valid starting port")
                return False

        if self.options['LastPort']['Value']:
            try:
                if int(self.options['LastPort']['Value']) > 65535 and int(self.options['LastPort']['Value'] < 0):
                    minus("Ports cannot be < than 0 or > than 65535")
                    return False
            except Exception:
                minus("Please insert a valid starting port")
                return False

        try:
            ipaddress.ip_address(self.options["Ip"]["Value"])
        except Exception:
            minus("The Ip address is not valid")
            return False
        return True

    def run(self):
        if not self.validate_options():
            return
        info("Starting port scan")
        open_ports = self.port_scan(self.options['Ip']['Value'], self.options['FirstPort']['Value'], self.options['LastPort']['Value'])
        if not open_ports:
            minus("Could not detect any open TCP ports")
        self.get_serv_details(self.options['Ip']['Value'], open_ports)

    def port_scan(self, ip, sport, eport):

        open_ports = []
        for port in range(int(sport), int(eport)):
            ports = threading.Thread(target=self.scan_port, args=(ip, port))
            ports.start()
            if ports is None:
                continue
            else:
                ports.join()
                open_ports.append(port)

        return open_ports

    def scan_port(self, ip, port):
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        try:
            result = socket_obj.connect_ex((ip, port))
            if result == 0:
                plus("Open port detected: Ip:" + str(ip) + " Port:" + str(port))
                self.log_to_file("Open port detected: Ip:" + str(ip) + " Port:" + str(port))
                self.screen_lock.aquire()
                return port
            else:
                return None
        except Exception:
            return None
        finally:
            socket_obj.close()
            self.screen_lock.release()
    
    def banner_grab(self, ip, port):
        banner_grab = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(2)

        try:
            banner_grab.connect_ex((ip, port))
            details = banner_grab.recv(1024)
            if details:
                plus(details.decode("utf-8"))
                self.log_to_file("Banner for port " + port + "\n" +  details.decode("utf-8"))
        except Exception:
            pass
        finally:
            banner_grab.close()

    def get_serv_details(self, ip, open_ports):
        for port in open_ports:
            queue = threading.Thread(target=self.banner_grab, args=(ip, port))
            queue.start()
            queue.join()
