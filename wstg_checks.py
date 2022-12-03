#!/usr/bin/env python
import subprocess
import requests
import json
from bs4 import BeautifulSoup, Comment

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
    return subprocess.run(["wafw00f", url])


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
    return subprocess.call(["nmap", url, "--script", " http-methods", "--script-args", "http-methods.test-all=true"])


def header_check(url):
    response = requests.get("https://" + url)

    required_headers = ["X-XSS Protection", "strict-transport-security", "content-security-policy", "cache-control",
                        "access-control-allow-origin", "x-frame-options", "x-content-type-options", "Referrer-Policy"]

    for h in required_headers:
        if h in response.headers:
            print(h + ":" + response.headers[h])
        else:
            print("Missing " + h)


def git_repo(url):
    response = requests.get("https://" + url + "/.git/config")

    if response.status_code == 200:
        print("Found git repo")


def look_for_comments(url):
    page = requests.get("https://" + url)
    soup = BeautifulSoup(page.content, "html.parser")

    for comments in soup.findAll(text=lambda text: isinstance(text, Comment)):
        print(comments.extract())


def get_meta_info(url):
    page = requests.get("https://" + url)
    soup = BeautifulSoup(page.content, "html.parser")

    for meta in soup.findAll("meta"):
        print(meta)


def cookies_check(url):
    # from packtpub
    req = requests.get("https://" + url)
    for cookie in req.cookies:
        print('Name:', cookie.name)
        print('Value:', cookie.value)

        if not cookie.secure:
            cookie.secure = '\x1b[31mFalse\x1b[39;49m'
        print('Secure:', cookie.secure)

        if 'httponly' in cookie._rest.keys():
            cookie.httponly = 'True'
        else:
            cookie.httponly = '\x1b[31mFalse\x1b[39;49m'
        print('HTTPOnly:', cookie.httponly)

        if cookie.domain_initial_dot:
            cookie.domain_initial_dot = '\x1b[31mTrue\x1b[39;49m'
        print('Loosly defined domain:', cookie.domain_initial_dot, '\n')


cookies_check("www.woolworths.com.au")
