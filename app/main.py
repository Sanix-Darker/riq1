import time

from utils import *
from settings import IP_LIST

# We print the presentation of the app
presentation()

# We update the ip list
update_ip_list(7)

print("[+] Your current Ip info:"+getIpInfo())

url = input("[+] Your url: ")

with open(IP_LIST, "r+") as fil_:
    ip_list = fil_.readlines()
    for ip in ip_list:
        time.sleep(1) # We wait 1s before proceed
        print("[+] Your current Ip info:"+getIpInfo(ip))
        res = sendGet(ip, url)
        print("[+] ------ Request sent successfully !\n")