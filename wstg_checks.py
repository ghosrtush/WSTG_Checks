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
        return "[-] Robots.txt not found"



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

def crossdomainpolicy(url):
    crossdomain = requests.get('https://' + url + '/crossdomain.xml')
    clientaccess = requests.get('https://' + url + '/clientaccesspolicy.xml')

    if crossdomain.status_code == 200:
        print(crossdomain.text)
    else:
        print("[-] crossdomain.xml not found")

    if clientaccess.status_code == 200:
        print(clientaccess.text)
    else:
        print("[-] clientaccesspolicy.xml not found")


def securitytxt(url):
    securitytxt = requests.get('https://' + url + '/security.txt')
    wellknown = requests.get('https://' + url + '/.well-known/security.txt')

    if securitytxt.status_code == 200:
        print(securitytxt.text)
    else:
        print("[-] security.txt not found")

    if wellknown.status_code == 200:
        print(wellknown.text)
    else:
        print("[-] /.well-known/security.txt not found")


def sitemap(url):
    sitemap = requests.get('https://' + url + '/sitemap.xml')

    if sitemap.status_code == 200:
        print(sitemap.text)
    else:
        print("[-] sitemap.xml not found")


def heartbleedcheck(url):
    print("[+] Scanning for Heartbleed")
    subprocess.call(["nmap", "-p", "443", url, "--script", " ssl-heartbleed", "--script-args", "vulns.showall"])
    # Maybe just grep for State:

def caacheck(url):
    subprocess.call(["host", "-t", "caa", url])



