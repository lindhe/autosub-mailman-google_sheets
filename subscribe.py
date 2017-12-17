#!/bin/python
# -*- coding: utf-8 -*-
#
# License: MIT
# Author: Andreas Lindhé

import sys
from bs4 import BeautifulSoup as bs
import requests as r

# Returns the response object after loggin in
# TODO: Check that login was successful
def login(password, domain, mailinglist):
  url = 'http://lists.' + domain + '/mailman/admin/' + mailinglist
  credentials = {'adminpw': password, 'admlogin': 'Let me in...'}
  res = r.post(url, credentials)
  return (res)

def goto_members():
  # open members management
  # open add new member
  return (0)

def subscribe():
  sub_page = membership_admin()
  token = get_csrf(sub_page)
  return (0)

def get_csrf(sub_page):
  return (0)

def logout():
  return (0)

def main():
  login()
  subscribe()
  logout()
  return (0)


if __name__ == '__main__':
    program = sys.argv[0]

    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("Interrupted\n")
        try:
            sys.exit(0)
        except SystemExit:
            sys.exit(1)

