import socket
import time

try:
    from settings import CHECK_PORT_RETRY, CHECK_PORT_DELAY, CHECK_PORT_TIMEOUT, CHECK_PORT_RECURRENT_PORT
except Exception as es:
    try:
        from app.settings import CHECK_PORT_RETRY, CHECK_PORT_DELAY, CHECK_PORT_TIMEOUT, CHECK_PORT_RECURRENT_PORT
    except Exception as es:
        print("[+] An error importing settings file!")
        exit()

start_port = 1
last_port = 99999
retry = CHECK_PORT_RETRY
delay = CHECK_PORT_DELAY
timeout = CHECK_PORT_TIMEOUT
recurrent_port = CHECK_PORT_RECURRENT_PORT

def isOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except Exception as es:
        return False
    finally:
        s.close()

def checkHost(ip, port):
    ipup = False
    for i in range(retry):
        if isOpen(ip, port):
            ipup = True
            break
        else:
            time.sleep(delay)
    return ipup


def checkLoop(ip, to_loop, from_recurrent=False):
    found, array_ = 0, []
    for port in to_loop:
        print("\r[+] Testing  "+ip+":"+str(port), end="")
        if checkHost(ip, port):
            found += 1
            print("\n[+] IP: "+ ip + " at "+str(port)+" is UP on this port\n")
            array_.append(ip+":"+str(port))
            if (from_recurrent==True):break
        if (found >= 3):break
    return array_


def checkIt(ip):
    """[summary]

    Arguments:
        ip {[string]} -- [description]
        last_port {[int]} -- [description]

    Returns:
        [string] -- [description]
    """
    if "." not in ip: return []
    array_ = checkLoop(ip, recurrent_port, True)
    if len(array_) > 0: return array_
    else: return []
    # return checkLoop(ip, range(start_port, last_port))

# print(checkIt(ip))