#!/usr/bin/env python3
import sys
from ciscoconfparse import CiscoConfParse
from netaddr import *
import sys

# Resources
# https://devcentral.f5.com/s/question/0D51T00006i7jW8SAI/python-show-runningconfig
# https://f5-sdk.readthedocs.io/en/latest/ F5 SDK documentation
# https://pypi.org/project/ciscoconfparse/ ciscoconfparse documentation
# This is the ugliest code I have ever hacked together. 
# Please refactor and document when time permits.

# parse = CiscoConfParse('10_105_96_36.f5bigip_full', syntax='junos', comment='#')
# parse = CiscoConfParse('testconfig.cfg', syntax='junos', comment='#')
parse = CiscoConfParse(sys.argv[1], syntax='junos', comment='#')
print(sys.argv[1])
device_id = sys.argv[1].split('.')[0]
urt_header = '''
# Additional routing lines from file /home/afa/.fa/firewalls/%s/additionalRoutes.urt
#	==========================================================
#	Firewall Analyzer: Routing	Table	for Firewall name: %s
#	Generated manually to support PBR
#	==========================================================
#
# Routes:
'''
print(urt_header %(device_id, device_id))

def get_next_hop_interface(next_hop_ip, parse):

    local_interfaces = parse.find_objects('net self 1*')
    for local_interface in local_interfaces:
        local_interface_ip_and_prefix_mask = local_interface.re_match_iter_typed(r'\s+address\s(.*)')
        local_interface_vlan = local_interface.re_match_iter_typed(r'\s+vlan\s(.*)')
        
        if IPAddress(next_hop_ip) in IPNetwork(local_interface_ip_and_prefix_mask):
            # print('match!!!')
            return local_interface_vlan

# for f5_virtual in parse.find_objects(r'ltm virtual.*policy_route'): # added multiple matches of VIP naming convention.
for f5_virtual in parse.find_objects('ltm virtual policy*'):
    #Find all default route pools
    virtual_destination_ip = f5_virtual.re_match_iter_typed(r'\s+destination\s(.*)', default="").split(':')[0]
    if "/" in virtual_destination_ip:
        virtual_destination_ip = virtual_destination_ip.split('/')[2]
    virtual_destination_mask = f5_virtual.re_match_iter_typed(r'\s+mask\s(.*)', default="")
    if virtual_destination_ip == "any":
        virtual_destination_ip = "0.0.0.0"
        virtual_destination_mask = "0.0.0.0"

    virtual_pool = f5_virtual.re_match_iter_typed(r'\s+pool\s(.*)', default="")
    virtual_source = f5_virtual.re_match_iter_typed(r'\s+source\s(.*)', default="")

    virtual_vlans = parse.find_object_branches(branchspec=(f5_virtual.text, r'vlans$',r'^\s+\S+'))


    if virtual_pool:
        pool = parse.find_object_branches(branchspec=('ltm pool ' + virtual_pool, r'members', r'\:', r'address'), regex_flags=0)
        for pool_members in pool:
            next_hop_ip = (((pool_members[3].text).strip()).split())[1]
            next_hop_local_interface = get_next_hop_interface(next_hop_ip, parse)
            for vlan in virtual_vlans:
                if vlan[2] is None:
                        print("%s %s %s %s %s -" % 
                            (
                            virtual_destination_ip, 
                            virtual_destination_mask, 
                            next_hop_ip, 
                            next_hop_local_interface, 
                            next_hop_local_interface, 
                            )
                        )
                else:
                    vlan_name = (vlan[2].text).strip()
                    print("%s %s %s %s %s %s" % 
                        (
                        virtual_destination_ip, 
                        virtual_destination_mask, 
                        next_hop_ip, 
                        next_hop_local_interface, 
                        next_hop_local_interface,
                        vlan_name
                        )
                    )



