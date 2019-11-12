from app.utils import *
import argparse

# Initialize the arguments
prs = argparse.ArgumentParser()
prs.add_argument('-u', '--url', help='The target URL', type=str, default="https://example.com")
prs.add_argument('-t', '--type', help='The type of the request (GET, POST)', type=str, default="get")
prs.add_argument('-i', '--nb_ip', help='The number of ip address you want them to perform the request', type=int, default=3)
prs.add_argument('-r', '--nb_request', help='The number of request that will be done per ip address', type=int, default=1)
prs = prs.parse_args()


if __name__ == "__main__":
    # We print the presentation of the app
    presentation()

    # We update the ip list
    update_ip_list(prs.nb_ip)

    # execute only if run as a script
    main_core(prs.nb_request, prs.url)