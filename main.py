import time

from utils import *

presentation()



print("[+] Your current Ip info:"+getIpInfo())

url = input("[+] Your url: ")

with open("./ips.txt", "r+") as fil_:
    ip_list = fil_.readlines()
    for ip in ip_list:
        time.sleep(1) # We wait 1s before proceed
        print("[+] Your current Ip info:"+getIpInfo(ip))
        res = sendGet(ip, url)
        print("[+] ------ Request sent successfully !\n")