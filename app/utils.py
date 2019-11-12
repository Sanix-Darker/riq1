import requests
import json
from lxml import html
import time
from os import path as ospath


from settings import IP_LIST, PROXY_VPN_LIST, MAXIMUM_LIFE

s = requests.Session()


def modification_date(filename):
    return ospath.getmtime(filename)


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
    r = s.get(url)
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
            time.sleep(0.5)


def update_ip_list(limit = None):
    print("[+] Fetching ip address, please wait a few seconds...")
    life = time.time() - modification_date(IP_LIST)

    num_line = 0
    with open(IP_LIST, "r+") as frr_check: num_line = len(frr_check.readlines())

    if ((life) > MAXIMUM_LIFE or num_line < 3): # if theipList file have more than 100s of life we erase
        print("[+] Will proceed on fetching new IP address, your ip_list life: "+str(life)+" seconds")
        print("[+] Press Ctrl+C to stop anytime the fetching process.")
        time.sleep(3)
        try:
            with open(PROXY_VPN_LIST, "r+") as frr:
                site_list = json.loads(frr.read())
                # We empty the file of ip
                with open(IP_LIST, "w+") as frr_erase: frr_erase.write("")
                count = 0
                stoploop = False
                for site in site_list:
                    # We stop the loop if we reach a nlimit number of ip address we wanted at the start
                    if limit != None or stoploop == True:
                        if count >= limit: break

                    r = requests.get(site["url"])
                    tree, type_ = html.fromstring(r.content), site['type']

                    # if ips are listed in a table and not referenced by a sepcific class or id
                    if type_ == "table":
                        print("[+] Type : table...")
                        tr_array = tree.xpath(site['tr_array'])
                        for tr in tr_array:
                            td_array = tr.xpath('./td//text()')
                            print("[+] td_array: ", td_array)
                            try:
                                ip, port, country = td_array[site['ip_address']], td_array[site['port']], td_array[site['country']]
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