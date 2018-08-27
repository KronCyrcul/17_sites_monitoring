from urllib.parse import urlparse
from urllib.request import urlopen
import datetime
import whois
import sys


def load_urls4check(path):
    try:
        with open(path, "r") as sites_file:
            sites = sites_file.read().split()
        return sites
    except FileNotFoundError:
        return None


def is_server_respond_with_200(url):
    server_response = urlopen(url).getcode()
    if server_response == 200:
        return True
    else:
        return False


def get_domain_expiration_date(domain_name):
    domain_info = whois.whois(domain_name)
    if type(domain_info["expiration_date"]) is list:
        return domain_info["expiration_date"][0]
    else:
        return domain_info["expiration_date"]


def print_site_health(url, server_response, time_before_expiration):
    print("Site URL: {}".format(url))
    print("Status code is 200: {}".format(server_response))
    print("Paid up front for a month: {}".format(time_before_expiration))


if __name__ == "__main__":
    try:
        filepath = sys.argv[1]
    except IndexError:
        sys.exit("Enter path to file")
    sites = load_urls4check(filepath)
    if sites is None:
        sys.exit("File not found")
    today = datetime.datetime.today()
    for site in sites:
        server_response = is_server_respond_with_200(site)
        domain_name = urlparse(site).hostname
        expiration_date = get_domain_expiration_date(domain_name)
        time_before_expiration = expiration_date - today
        if time_before_expiration.days > 31:
            is_payed_up_front = "Yes,{} days before expiration".format(
                time_before_expiration.days)
        else:
            is_payed_up_front = "No,expired {} days ago".format(
                time_before_expiration.days*-1)
        print_site_health(site, server_response, is_payed_up_front)
