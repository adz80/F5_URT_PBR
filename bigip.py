from f5.bigip import ManagementRoot
import json

# Connect to the BigIP
# mgmt = ManagementRoot("bigip.example.com", "admin", "somepassword")
f = open('f5sample.json',)
mgmt = json.load(f)

print(mgmt)

# Get a list of all pools on the BigIP and print their names and their
# members' names

# pools = mgmt.tm.ltm.pools.get_collection()
# for pool in pools:
#     print pool.name
#     for member in pool.members_s.get_collection():
#          print member.name
