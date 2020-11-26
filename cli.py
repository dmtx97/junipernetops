from junipernetops.juniper import Juniper
import json
import argparse
import sys

def audit_interfaces(switch, enabled_interfaces, interface_to_status):

    count = sum(1 for i in enabled_interfaces if i in interface_to_status and interface_to_status[i] == 'inactive')

    print("Number of enabled interfaces with port security for {} : {}\n".format(switch.host_name, count))

    interfaces = []
    if count > 0 :
        for i in enabled_interfaces:
            if i in interface_to_status and interface_to_status[i] == 'inactive':
                interfaces.append(i)
    
    return interfaces


def switches_to_list():

    switches = []

    # CONSTANT list of omitted buildings
    SKIPPED_BUILDINGS = ['Townhomes', 'Horner Ballpark',]

    with open('./data/input/switches.json', 'r') as f:
        data = json.loads(f.read())
    
        for key in data:
            for value in data[key]:
                if value['host_name'] not in SKIPPED_BUILDINGS:
                    
                    switch = Juniper(value['host_name'], value['host_address'], secrets.username, secrets.password)
                    switches.append(switch)

    return switches

def output_audit():
    output_json = {}
    swlist = switches_to_list()

    for sw in swlist:
        try:
            enabled_interfaces = sw.get_enabled_interfaces()
            interface_to_status = sw.get_ethernet_switching_options()
            print("Scanning {} for port security".format(sw.host_name))
            output_json[sw.host_name] = {}
            output_json[sw.host_name]['ipaddress'] = sw.host_address
            output_json[sw.host_name]['ports'] = audit_interfaces(sw, enabled_interfaces, interface_to_status)  
    
        except:
            print("Could Not Connect To Device")
            pass

    # filename = "./data/output/port-security-audit-{}.json".format(datetime.now().strftime("%m-%d-%Y"))
    filename = "./data/output/port-security-audit.json"
    with open(filename, 'w') as f:
        json.dump(output_json, f, indent=4)


def activate_security():
    with open('./data/output/port-security-audit.json', 'r') as f:
        data = json.loads(f.read())
        for building in data:
            address = data['building']['ipaddress']
            ports = data[building]['ports']
            if(len(ports) > 0):
                sw = Juniper(building, address, secrets.username, secrets.password)
                sw.activate_port_security(ports)

def main():

    parser = argparse.ArgumentParser()

    FUNCTIONMAP = {'outputaudit' : output_audit, 'activatesecurity' : activate_security}
    
    parser.add_argument('command', choices=FUNCTIONMAP.keys())

    args = parser.parse_args()

    func = FUNCTIONMAP[args.command]

if __name__ == "__main__":
    sys.exit(func())
