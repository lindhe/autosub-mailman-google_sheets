#!/bin/python
# -*- coding: utf-8 -*-
#
# License: MIT
# Author: Andreas Lindhé

import sys
from bs4 import BeautifulSoup as bs
import requests as r

VERBOSE = True

def vprint(string):
  if VERBOSE:
    print(string)

# Returns the login cookie token
def login(domain, mailinglist, password):
  url = 'http://lists.' + domain + '/mailman/admin/' + mailinglist
  credentials = {'adminpw': password, 'admlogin': 'Let me in...'}
  res = r.post(url, credentials)
  res.raise_for_status()
  vprint("Login successful!")
  return (res.cookies[mailinglist + '+admin'])

def membership_admin():
  # open members management
  # open add new member
  return (0)

def subscribe(domain, mailinglist, token):
  sub_page = membership_admin()
  token = get_csrf(sub_page)
  return (0)

def get_csrf(sub_page):
  return (0)

def logout():
  return (0)

  token = login(domain, mailinglist, password)
  subscribe(domain, mailinglist, token)
  logout()
def main(domain, mailinglist, password, members_file):
  return (0)


if __name__ == '__main__':
    program = sys.argv[0]

    if len(sys.argv) >= 5:
        d  = sys.argv[1]
        ml = sys.argv[2]
        pw = sys.argv[3]
        mf = sys.argv[4]
    else:
        print("Usage: " + program + " example.com list_name password email_list_file")
        exit(1)

    try:
        main(d, ml, pw, mf)
    except KeyboardInterrupt:
        sys.stderr.write("Interrupted\n")
        try:
            sys.exit(0)
        except SystemExit:
            sys.exit(1)

