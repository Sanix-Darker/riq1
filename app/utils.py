import requests
import json
from lxml import html
import time
from os import path as ospath
from sys import exit

import js2py

try: from settings import IP_LIST, PROXY_VPN_LIST, MAXIMUM_LIFE
except Exception as es:
    try:
        from app.settings import IP_LIST, PROXY_VPN_LIST, MAXIMUM_LIFE
    except Exception as es:
        print("[+] An error importing settings file!")
        exit()

s = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def modification_date(filename):
    if ospath.exists(filename) == False:
        with open(filename, "w+") as fik:
            fik.write("")
    return ospath.getmtime(filename)


def getIpInfo(ip=None):
    """[summary]

    Keyword Arguments:
        ip {[type]} -- [description] (default: {None})

    Returns:
        [type] -- [description]
    """
    print("[+] ip:",ip)
    if ip != None: rr = requests.get("https://ipinfo.io/"+ip.split(":")[0]+"/geo", headers=headers)
    else: rr = requests.get("https://ipinfo.io/", headers=headers)

    try: return json.dumps(json.loads(rr.content), indent=4, sort_keys=True)
    except Exception as es: return "{}"


def presentation():
    print("\n")
    print("[+] -------------------------")
    print("[+] --- |  _ \(_) __ _/ | ---")
    print("[+] --- | |_) | |/ _` | | ---")
    print("[+] --- |  _ <| | (_| | | ---")
    print("[+] --- |_| \_\_|\__, |_| ---")
    print("[+]                 |_|      ")
    print("[+] ----------------- by S@n1x-d4rk3r ")
    print("\n[+] Note: This program can send the same request multiple time by changing ip_address each time.")



def sendGet(ip, url):
    """[summary]

    Arguments:
        ip {[type]} -- [description]
        url {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    s.proxies = {"http": "http://"+ip+"/"}
    r = s.get(url, headers=headers)
    return r.text



def if_ipaddress_return_it(ip):
    try:
        parts = ip.split('.')
        return len(parts) == 4 and all(0 <= int(part) < 256 for part in parts)
    except ValueError: return False # one of the 'parts' not convertible to integer
    except (AttributeError, TypeError): return False # `ip` isn't even a string



def save_ip(ip, port, country=""):
    if (if_ipaddress_return_it(ip)): # if the ip is valid
        with open(IP_LIST, "a+") as frr2:
            frr2.write(ip+":"+port+"#"+country+"\n")
            print("[+] Saving '"+ip+":"+port+"#"+country+"'")
            print("[+] Press Ctrl+C to stop anytime the fetching process.")
            print("[+] ----")
            time.sleep(0.2)



def update_ip_list(limit = None):
    print("[+] Fetching ip address, please wait a few seconds...")
    life = time.time() - modification_date(IP_LIST)

    num_line = 0
    with open(IP_LIST, "r+") as frr_check: num_line = len(frr_check.readlines())

    if ((life) > MAXIMUM_LIFE or num_line < 3): # if theipList file have more than 100s of life we erase
        print("[+] Will proceed on fetching new IP address, your ip_list life: "+str(life)+" seconds")
        print("[+] Press Ctrl+C to stop anytime the fetching process.")
        time.sleep(1)
        try:
            with open(PROXY_VPN_LIST, "r+") as frr:
                site_list = json.loads(frr.read())
                # We empty the file of ip
                with open(IP_LIST, "w+") as frr_erase:
                    frr_erase.write("")

                count, stoploop = 0, False
                for site in site_list:
                    # We stop the loop if we reach a nlimit number of ip address we wanted at the start
                    if limit != None or stoploop == True:
                        if count >= limit: break

                    r = requests.get(site["url"], headers=headers)
                    tree, type_ = html.fromstring(r.content), site['type']

                    # if ips are listed in a table and not referenced by a sepcific class or id
                    if type_ == "table":
                        print("[+] Type : table...")
                        tr_array = tree.xpath(site['tr_array'])
                        for tr in tr_array:
                            td_array = tr.xpath('./td//text()')
                            for i, td_ in enumerate(td_array):
                                td_array[i] = td_.replace("\r", "").replace("\t", "").replace("\n", "").replace("\\r", "").replace("\\t", "").replace("\\n", "").replace(" ", "")

                            print("[+] td_array: ", td_array)
                            try:
                                site_ip_address = ""
                                # print("[+] site_ip_address: ", td_array[site['ip_address']])
                                if "document." in td_array[site['ip_address']]:
                                    site_ip_address_to_evaluate = td_array[site['ip_address']].replace("document.write(", "function r(){return ").replace(");", ";}r()").replace("r(;}", "")
                                    # print("[+] site_ip_address_to_evaluate: ", site_ip_address_to_evaluate)
                                    site_ip_address = js2py.eval_js(site_ip_address_to_evaluate)
                                else:
                                    site_ip_address = td_array[site['ip_address']]

                                # print("[+] site_ip_address: ", site_ip_address)

                                ip, port, country = site_ip_address, td_array[site['port']], td_array[site['country']]
                                print(ip, port, country)
                                save_ip(ip, port, country)
                                # We stop the loop if we reach a nlimit number of ip address we wanted at the start
                                if limit != None:
                                    if count >= limit:
                                        stoploop = True
                                        break
                                count += 1
                            except Exception as es: pass
                    else: # For the specific referencing
                        try:
                            ip_address, ports, countries = tree.xpath(site['ip_address']), tree.xpath(site['port']), tree.xpath(site['country'])
                            for i, ip in enumerate(ip_address): save_ip(ip, ports[i], countries[i])
                        except Exception as es: pass

        except KeyboardInterrupt as es: print("[+] Stoping the fetching.")
    else:
        print("[+] Escape the fetching of ip address, it's too early, the life : "+str(life)+" seconds")



def sendRequests(url, nb_request):
    """[summary]

    Arguments:
        IP_LIST {[type]} -- [description]
        url {[type]} -- [description]
        nb_request {[type]} -- [description]
    """
    print("[+] IP_LIST: ", IP_LIST)
    print("[+] Your current Ip info:"+getIpInfo())
    with open(IP_LIST, "r+") as fil_:
        for ip in fil_.readlines():
            for i in range(0, nb_request):
                print("\n[+] -------------------------")
                print("[+] New IP info:"+getIpInfo(ip))
                res = sendGet(ip, url)
                print("[+] -- Request ["+str(i)+"], ip: ["+str(ip)+"], url: ["+str(url).replace("\n", "").replace("\\n", "")+"] sent successfully !\n")



def main_core(nb_request, url):
    """[The main process]

    Arguments:
        nb_request {[type]} -- [description]
        url {[type]} -- [description]
    """
    sendRequests(url, nb_request)