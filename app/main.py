import time

from utils import *
from settings import IP_LIST

# We print the presentation of the app
presentation()

# We update the ip list
update_ip_list(7)

print("[+] Your current Ip info:"+getIpInfo())

url = input("[+] Your url: ")

nb_request = int(input("[+] THe number of request per IP you want: "))

sendRequests(IP_LIST, url, nb_request)