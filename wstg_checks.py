#!/usr/bin/env python

import subprocess


def whatweb_scan(url):
    whatweb = subprocess.run(['whatweb', url], capture_output=True)
    return print(whatweb.stdout.decode("utf-8"))

whatweb_scan("google.com")


# banner grabbing