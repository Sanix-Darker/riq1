import requests
import json
from lxml import html
import re

s = requests.Session()

def getIpInfo(ip=None):
    """[summary]

    Keyword Arguments:
        ip {[type]} -- [description] (default: {None})

    Returns:
        [type] -- [description]
    """
    if ip != None: rr = requests.get("https://ipinfo.io/"+ip.split(":")[0]+"/geo")
    else: rr = requests.get("https://ipinfo.io/")

    return json.dumps(json.loads(rr.content), indent=4, sort_keys=True)


def presentation():

    print("[+] --- |  _ \(_) __ _/ | ---")
    print("[+] --- | |_) | |/ _` | | ---")
    print("[+] --- |  _ <| | (_| | | ---")
    print("[+] --- |_| \_\_|\__, |_| ---")
    print("[+]                 |_|      ")
    print("[+] ----------------- by S@n1x-d4rk3r ")
    print("\n[+]  Note: This program can send multiple by changing ipaddress each time")


def sendGet(ip, url):
    """[summary]

    Arguments:
        ip {[type]} -- [description]
        url {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    s.proxies = {"http": "http://"+ip+"/"}
    r = s.get(url)
    return r.text


def if_ipaddress_return_it(ip):
    aa=re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",ip)
    if aa: return aa.group()
    return ""

def updateIpList():
    print("[+] Fetching ip address, please wait a few seconds...")
    with open("proxy_vpn_fetch.json", "r+") as frr:
        site_list = json.loads(frr.read())
        for site in site_list:
            r = requests.get(site["url"])
            tree = html.fromstring(r.content)
            ip_address = tree.xpath(site['ip_address'])
            ports = tree.xpath(site['port'])
            countries = tree.xpath(site['country'])
            for i, ip in enumerate(ip_address):
                if len(if_ipaddress_return_it(ip)) > 0:
                    with open("./ips.txt", "r+") as frr2:
                        frr2.write(ip+":"+ports[i]+"#"+countries[i])