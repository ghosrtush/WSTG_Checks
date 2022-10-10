#!/usr/bin/env python
import subprocess
import requests
import json

WHATWEB_API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'


def whatweb_scan(url):
    whatweb = subprocess.run(['whatweb', url], capture_output=True)
    return whatweb.stdout.decode("utf-8")


def robots_check(url):
    robots = requests.get('https://' + url + '/robots.txt')
    if robots.status_code == 200:
        return robots.text
    else:
        return "Robots.txt not found"


# banner grabbing for  server versions + info leakage

# http headers checks
# def header_checks(url):


# Connect to url
# iterate through headers
# check for the list of headers
# call out missing headers
# call out misconfigured headers ie csp 'inline' etc


# response.headers

# cookie status - after login?s


# wafw00f - check for WAF in use


def wapalyzer(url):
    url_lookup = "https://api.wappalyzer.com/v2/lookup/?urls=" + url
    headers = {
        'x-api-key': WHATWEB_API_KEY
    }
    response = requests.request("GET", url_lookup, headers=headers)
    response_dict = response.json()
    prettyfied_dict = json.dumps(response_dict, indent=4)
    return prettyfied_dict
    # TODO : Extract name and version from JSON
