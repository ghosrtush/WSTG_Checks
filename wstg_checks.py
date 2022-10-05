#!/usr/bin/env python

import subprocess
import requests
def whatweb_scan(url):
    whatweb = subprocess.run(['whatweb', url], capture_output=True)
    return whatweb.stdout.decode("utf-8")


def robots_check(url):
    robots = requests.get('https://'+url+'/robots.txt')
    if robots.status_code == 200:
        return robots.text
    else:
        return "Robots.txt not found"

# banner grabbing for  server versions + info leakage

# http headers checks

# cookie status - after login?s


# wafw00f - check for WAF in use



print("[+] WhatWeb Results")
print(whatweb_scan("google.com"))
print("[+] Robots.txt check")
print(robots_check('google.com'))