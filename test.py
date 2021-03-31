#!/usr/bin/env python3 
import dumper
from ciscoconfparse import CiscoConfParse
from operator import attrgetter

'''
Please see dcumnetation for Cisco Conf Parse on functions that are used.

http://www.pennington.net/py/ciscoconfparse/api_CiscoConfParse.html




'''


parse = CiscoConfParse('10_105_96_36.f5bigip_full', syntax='junos', comment='#')


while True:
    branchspec = (r'ltm\spool\sCCB_VIP_10.117.124.20_5012_pool', r'members', r'\S+?:\d+', r'state\sup')
    branches = parse.find_object_branches(branchspec=branchspec)

    # print(branches[0][0])
    # pool = parse.find_objects('policy_route_NSA_ANA_all_Tier2_to_FW_pool')
    # dumper(pool)
    # pool_ip = pool.re_match_iter_typed('\s+members\s(.*)', default="")


    # converted = convert_braces_to_ios(parse, stop_width=4)
    converted = parse.find_all_children(r'ltm\spool\sCCB_VIP_10.117.124.20_5012_pool', exactmatch=False, ignore_ws=False)
    converted2 = parse.find_blocks(r'ltm pool CCB_VIP_10.117.124.20_5012_pool', exactmatch=False, ignore_ws=False)
    converted3 = parse.find_blocks(r'members', exactmatch=False, ignore_ws=False)

    pool = parse.find_object_branches(branchspec=(r'CCB_VIP_10.117.124.20_5012_pool', r'members', r'\:', r'address'), regex_flags=0)
    for pool_members in pool:
        print((((pool_members[3].text).strip()).split())[1])
    
    
    
    
    # pool_members = 
    # for x in pool_members[x]:
    #     print(pool_members[x][3].text)
    
    
    # print(converted4[0][3].text.strip.split())


# , r'members', r'\:', r'address'
    # test = converted4[0][3].text



# for x in pool_members:
#     print(pool_members[2])

