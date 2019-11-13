import requests
import json
from lxml import html
import time
from os import path as ospath
from sys import exit

import random

import js2py

try:
    from settings import IP_LIST, PROXY_VPN_LIST, MAXIMUM_LIFE
    from checkport import *
except Exception as es:
    try:
        from app.settings import IP_LIST, PROXY_VPN_LIST, MAXIMUM_LIFE
        from app.checkport import *
    except Exception as es:
        print("[+] An error importing settings file!")
        exit()

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

    if ip != None:
        print("[+] - Ip:",ip)
        rr = requests.get("https://ipinfo.io/"+ip.split(":")[0]+"/geo")
    else: rr = requests.get("https://ipinfo.io/")

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
    s = requests.Session()
    s.proxies = {
        "http": "http://"+ip+"/",
        "https": "http://"+ip+"/",
    }
    r = s.get(url, headers=headers)
    return r.text



def if_ipaddress_return_it(ip):
    try:
        parts = ip.split('.')
        return len(parts) == 4 and all(0 <= int(part) < 256 for part in parts)
    except ValueError: return False # one of the 'parts' not convertible to integer
    except (AttributeError, TypeError): return False # `ip` isn't even a string



def save_ip(ip, port, country=""):
    print("[+]", ip, port, country)
    ip, port, country = str(ip), str(port), str(country)
    if (if_ipaddress_return_it(ip)): # if the ip is valid
        with open(IP_LIST, "a+") as frr2:
            frr2.write(ip+":"+port+"#"+country+"\n")
            print("[+] Saving '"+ip+":"+port+"#"+country+"'")
            print("[+] Press Ctrl+C to stop anytime the fetching process.")
            print("[+] ----")
            time.sleep(0.2)



def update_ip_list(limit = None):
    if limit == 0: limit = 1
    print("[+] ---")
    print("[+] Fetching ip address, please wait a few seconds...")
    life = time.time() - modification_date(IP_LIST)

    num_line = 0
    with open(IP_LIST, "r+") as frr_check: num_line = len(frr_check.readlines())

    if ((life) > MAXIMUM_LIFE or num_line < 5): # if theipList file have more than 100s of life we erase
        print("[+] Will proceed on fetching new IP address, your ip_list life: "+str(life)+" seconds")
        print("\n[+] Press Ctrl+C to stop anytime the fetching process.")

        try:
            with open(PROXY_VPN_LIST, "r+") as frr:
                site_list = json.loads(frr.read())

                # We shuffle the array
                random.shuffle(site_list)
                random.shuffle(site_list)

                # We empty the file of ip
                with open(IP_LIST, "w+") as frr_erase:
                    frr_erase.write("")

                count, stoploop = 0, False
                for site in site_list:
                    print("[+] URL-TO-FETCH:", site["url"], "Ctrl+C to skip this URL to another")
                    try:
                        # We stop the loop if we reach a nlimit number of ip address we wanted at the start
                        if limit != None and stoploop == True:
                            if count >= limit: break

                        r = requests.get(site["url"], headers=headers)
                        tree, type_ = html.fromstring(r.content), site['type']

                        # if ips are listed in a table and not referenced by a sepcific class or id
                        if type_ == "table" or type_ == "table_port_hide":
                            # print("[+] Type : table...")
                            tr_array = tree.xpath(site['tr_array'])
                            count_to_shutdown_from_checkport = 0
                            # print("[+] tr_array: ", tr_array)
                            for ii, tr in enumerate(tr_array):
                                td_array = tr.xpath('./td//text()')
                                for i, td_ in enumerate(td_array):
                                    td_array[i] = td_.replace("\r", "").replace("\t", "").replace("\n", "").replace("\\r", "").replace("\\t", "").replace("\\n", "").replace(" ", "")

                                # print("[+] td_array: ", td_array)
                                if len(td_array) > 2:
                                    try:
                                        site_ip_address, port_, country_ = "", "", ""

                                        if (type_ != "table_port_hide"):
                                            if site['port'] == -1: port_ = tr.xpath(site['port_selector'])
                                            else: port_ = td_array[site['port']]

                                        if site['country'] == -1: country_ = tr.xpath(site['country_selector'])
                                        else: country_ = td_array[site['country']]

                                        if site['ip_address'] == -1:
                                            if (type_ == "table_port_hide"):
                                                site_ip_address = td_array[1]
                                                chk_port = checkIt(site_ip_address)
                                                if len(chk_port) > 0:
                                                    port_ = chk_port[0].split(":")[1]
                                                    count_to_shutdown_from_checkport += 1

                                                if count_to_shutdown_from_checkport >= 2: break
                                            else:
                                                site_ip_address = tr.xpath(site['ip_address_selector'])
                                        else:
                                            # print("[+] site_ip_address: ", td_array[site['ip_address']])
                                            if "document." in td_array[site['ip_address']]:
                                                site_ip_address_to_evaluate = td_array[site['ip_address']].replace("document.write(", "function r(){return ").replace(");", ";}r()").replace("r(;}", "")

                                                site_ip_address = js2py.eval_js(site_ip_address_to_evaluate)
                                            else:
                                                site_ip_address = td_array[site['ip_address']]

                                        # print("[+] site_ip_address: ", site_ip_address) # ip_address_selector

                                        if "." in site_ip_address: # si on a des points dans ll'adresse
                                            save_ip(site_ip_address, port_, str(country_).replace("['", "").replace("']", "").replace(" ", ""))
                                            # We stop the loop if we reach a nlimit number of ip address we wanted at the start
                                            if limit != None:
                                                if count >= limit:
                                                    stoploop = True
                                                    break
                                            count += 1
                                    except: pass

                        elif type_ == "json_api":

                            for i in range(site['nb_call']):
                                try:
                                    ojson = json.loads(requests.get(site['url']).content.decode('utf-8'))
                                    save_ip(ojson[site["ip_address_key"]], ojson[site["port_key"]], ojson[site["country_key"]])
                                    if limit != None:
                                        if count >= limit:
                                            stoploop = True
                                            break
                                    count += 1
                                except: pass

                        elif type_ == "json":

                            object_array = tree.xpath(site['object_array'])
                            obj_brak, obj_json_elt = False, "["
                            # print("object_array: ", object_array)
                            for i, obj_element in enumerate(object_array):
                                if i > 0 and i < (len(object_array)-5):
                                    for obj in obj_element:
                                        if not obj_brak:
                                            if '{' in obj:
                                                obj_brak = True
                                                obj_json_elt += '{'
                                        elif '}' in obj:
                                            obj_brak = False
                                            obj_json_elt += '},'
                                        else:
                                            obj_json_elt += obj
                            obj_json_elt += "]"
                            obj_json_elt = json.loads(obj_json_elt.replace("},]", "}]"))

                            for ojson in obj_json_elt:
                                save_ip(ojson[site["ip_address_key"]], ojson[site["port_key"]], ojson[site["country_key"]])
                                if limit != None:
                                    if count >= limit:
                                        stoploop = True
                                        break
                                count += 1
                            # print("\n\n>>>>>>> obj_json_elt: ", obj_json_elt)
                        else: # For the specific referencing
                            try:
                                ip_address, ports, countries = tree.xpath(site['ip_address']), tree.xpath(site['port']), tree.xpath(site['country'])
                                for i, ip in enumerate(ip_address): save_ip(ip, ports[i], countries[i])
                            except Exception as es: pass
                    except KeyboardInterrupt as es: pass
        except KeyboardInterrupt as es: print("[+] Stoping the fetching.")
    else: print("[+] Escape the fetching of ip address, it's too early, the life : "+str(life)+" seconds")



def sendRequests(url, nb_request, limit=None):
    """[summary]

    Arguments:
        IP_LIST {[type]} -- [description]
        url {[type]} -- [description]
        nb_request {[type]} -- [description]
    """
    #print("[+] Your current Ip info:"+getIpInfo())
    print("[+] ==========================================================================")
    with open(IP_LIST, "r+") as fil_:
        ip_list_array = fil_.readlines()
        random.shuffle(ip_list_array)
        random.shuffle(ip_list_array)
        random.shuffle(ip_list_array)
        count = 0
        stoploop = False
        for ip in ip_list_array:

            if (stoploop == True): break

            for i in range(0, nb_request):
                print("\n[+] ------------------------------")
                print("[+] - New IP info:"+getIpInfo(ip))
                res = sendGet(ip, url)
                print("[+] - Request ["+str(i+1)+"], ip: ["+str(ip).replace("\n", "").replace("\\n", "")+"], url: ["+str(url)+"], length: "+str(len(res))+" !")
                if len(res) < 1000:
                    print("[+] - Res: ", res)
                print("[+] --------------------------------\n")
                if limit != None:
                    if count >= limit:
                        stoploop = True
                        break
                count += 1



def main_core(nb_request, url, limit=None):
    """[The main process]

    Arguments:
        nb_request {[type]} -- [description]
        url {[type]} -- [description]
    """
    sendRequests(url, nb_request, limit)