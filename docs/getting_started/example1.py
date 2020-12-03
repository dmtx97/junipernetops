from netopsauto.juniper import Juniper
from pprint import pprint

switch = Juniper("host_name", "host_address", "user", "password")

# We can optionally call initialize_device() to directly utilize the PyEZ Device instance

dev = switch.initialize_device()

dev.open()

pprint(dev.facts)

dev.close()

# prints detailed Juniper device information 
# https://www.juniper.net/documentation/en_US/junos-pyez/topics/task/program/junos-pyez-program-device-connecting.html