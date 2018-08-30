from urllib.parse import urlparse
import requests
import datetime
import whois
import sys


def load_urls4check(path):
    try:
        with open(path, "r") as sites_file:
            urls = sites_file.read().split()
        return urls
    except FileNotFoundError:
        return None


def is_server_respond_with_ok(url):
    try:
        server_response = requests.get(url)
        return server_response.ok
    except requests.exceptions.RequestException:
        return False


def get_domain_expiration_date(domain_name):
    try:
        domain_info = whois.whois(domain_name)
        if type(domain_info["expiration_date"]) is list:
            return domain_info["expiration_date"][0]
        else:
            return domain_info["expiration_date"]
    except whois.parser.PywhoisError:
        return False


def check_expiration_date(expiration_date, today, days_count):
    try:
        time_before_expiration = expiration_date - today
        return time_before_expiration.days >= days_count
    except TypeError:
        return False


def print_site_health(url, server_response, paid_up_front,
        today, expiration_date):
    print("Site URL: {}".format(url))
    print("Status code is 200: {}".format(server_response))
    if paid_up_front:
        print("Paid up front for a month: Yes,{} days before expire".format(
            (expiration_date-today).days))
    else:
        print("Paid up front for a month: {}".format(
            paid_up_front))


if __name__ == "__main__":
    try:
        filepath = sys.argv[1]
    except IndexError:
        sys.exit("Enter path to file")
    urls = load_urls4check(filepath)
    if urls is None:
        sys.exit("File not found")
    today = datetime.datetime.today()
    days_count = 31
    for url in urls:
        server_response = is_server_respond_with_ok(url)
        domain_name = urlparse(url).hostname
        expiration_date = get_domain_expiration_date(domain_name)
        paid_up_front = check_expiration_date(
            expiration_date,
            today,
            days_count)
        print_site_health(
            url,
            server_response,
            paid_up_front,
            today,
            expiration_date)
