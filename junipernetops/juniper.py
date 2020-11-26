from jnpr.junos.utils.start_shell import StartShell
from jnpr.junos.utils.config import Config
from jnpr.junos import Device
from paramiko import AuthenticationException
from lxml import etree
from xml.etree import ElementTree
import json
import sys
import re

class Juniper:
    def __init__(self, host_name, host_address, user, password):
        self.host_address = host_address
        self.user = user
        self.password = password
        self.host_name = host_name

    def initialize_device(self):
        dev = Device(host = self.host_address, user = self.user, password = self.password)
        return dev

    def get_enabled_interfaces(self):
        # Function returns list of Physical Interfaces which read 'Enabled, Physical link is Down'
        dev = self.initialize_device()
        ss = StartShell(dev)
        ss.open()
        cmd = ss.run('cli -c "show interfaces | match Physical | no-more"')
        ss.close()

        enabled_interfaces = []
        unchecked_interfaces = ['ae0', 'ae1', 'ae2', 'ae3', 'ae4', 'me0', 'vme']
        for line in cmd[1].splitlines():

            if "Enabled, Physical link is Down" in line:
                val = line.split("Physical interface: ")[1]
                val = val.split(", Enabled, Physical link is Down")[0]

                if not val in unchecked_interfaces:
                    enabled_interfaces.append(val + '.0')

        return enabled_interfaces

    def get_ethernet_switching_options(self):

        # Function returns ports with ethernet-switching-options and their status (active or inactive)
        dev = self.initialize_device()
        dev.open()
        filter = '<configuration><ethernet-switching-options/></configuration>'
        
        data = dev.rpc.get_config(filter_xml=filter)
        xml = etree.tostring(data, encoding='unicode', pretty_print=True)
        dom = ElementTree.fromstring(xml)

        ethernet_options_interfaces = dom.findall('ethernet-switching-options/secure-access-port/interface')

        interface_to_status = {}
        for i in ethernet_options_interfaces:

            if 'inactive' not in i.attrib.keys():
                interface_to_status[i.find("name").text] = "active"

            else:
                interface_to_status[i.find("name").text] = "inactive"

        dev.close()

        return interface_to_status

    def get_port_actions(self):
        
        dev = self.initialize_device()
        dev.open()
        filter = '<configuration><ethernet-switching-options/></configuration>'
        
        data = dev.rpc.get_config(filter_xml=filter)
        xml = etree.tostring(data, encoding='unicode', pretty_print=True)
        dom = ElementTree.fromstring(xml)

        ethernet_options_interfaces = dom.findall('ethernet-switching-options/secure-access-port/interface')

        interface_to_status = {}
        for i in ethernet_options_interfaces:

            if i.find('mac-limit/action') is not None:
                print(i.find('name').text)

    def activate_port_security(self, port_list):

        print("Connecting to : {}".format(self.host_name))
        device = self.initialize_device().open()
        cu = Config(device)

        for port in port_list:

            try:
                print("Activating security on port {}".format(port))
                set_command = 'activate ethernet-switching-options secure-access-port interface {}'.format(port)

                cu.load(set_command, format='set')

                if(cu.commit_check()):
                    cu.commit()

            except Exception as e:
                print(e)
                pass

        device.close()
        
    def change_password(self, user, password):

        device = self.initialize_device().open()
        cu = Config(dev)

        set_command = 'set system login user {} authentication encrypted-password {}'.format(user, password)

        cu.load(set_command, format='set')
        cu.commit()

        device.close()

    def set_rescue_config(self):
        dev = self.initialize_device()
        ss = StartShell(dev)

        ss.open()
        cmd = ss.run('cli -c "request system configuration rescue save"')
        ss.close()