#
# Some settings here for global variables
#
import os

IP_LIST = "./data/ips.txt"
PROXY_VPN_LIST = "./data/proxy_vpn_fetch.json"
MAXIMUM_LIFE = 100

# Checkport
CHECK_PORT_RETRY = 2
CHECK_PORT_DELAY = 3
CHECK_PORT_TIMEOUT = 2
CHECK_PORT_RECURRENT_PORT = [80, 808, 443, 8181, 8080, 6868, 8081, 8213, 51517, 3128, 35723, 1080,\
                            49022, 48213, 56696, 33735, 4145, 44391, 3121, 32529, 47552,\
                            35406, 50162, 41353, 35931,9991,\
                            53078, 8811, 44017, 46573, 50136, 61910, 59033, 49929, 34815,\
                            51184, 39364, 42287, 40714, 52148, 53879, 60678, 50204, 58912]