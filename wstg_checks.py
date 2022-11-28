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


def check_waf(url):
    return subprocess.run(["wafw00f",url])


def wapalyzer(urnl):
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


def poodle_check(url):
    print("[+] Scanning for Poodle")
    return subprocess.call(["nmap", "-p", "443", url, "--script", " ssl-poodle", "--script-args", "vulns.showall"])
    # Maybe just grep for State:


def caacheck(url):
    return subprocess.call(["host", "-t", "caa", url])


def dnssec(url):
    return subprocess.call(["host", "-t", "dnskey", url])

def sslchecks(url):
    return subprocess.call(["sslyze", url])

def check_http_methods(url):
    return subprocess.call(["nmap",  url, "--script", " http-methods", "--script-args", "http-methods.test-all=true"])

def header_check(url):
    response = requests.get("https://" + url)

    required_headers =["X-XSS Protection", "strict-transport-security", "content-security-policy", "cache-control", "access-control-allow-origin", "x-frame-options","x-content-type-options", "Referrer-Policy"]
    depreciated_headers = ["x-content-security-policy"]

    for h in required_headers:
        if h in response.headers:
            print(h + ":" + response.headers[h])
        else:
            print("Missing " + h)


