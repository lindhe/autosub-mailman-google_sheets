#!/bin/python
# -*- coding: utf-8 -*-
#
# License: MIT
# Author: Andreas Lindhé

import sys
from bs4 import BeautifulSoup as bs
import requests as r

VERBOSE = True

sub_config = {
    'csrf_token': '',
    'subscribe_or_invite': 0,
    'send_welcome_msg_to_this_batch': 0,
    'send_notifications_to_list_owner': 0,
    'subscribees': '',
    'invitation': '',
    'setmemberopts_btn': 'Submit Your Changes'
    }


def vprint(string):
  if VERBOSE:
    print(string)

# Returns session cookie and csrf_token
def login(domain, mailinglist, password):
  url = 'http://lists.' + domain + '/mailman/admin/' + mailinglist
  credentials = {'adminpw': password, 'admlogin': 'Let me in...'}
  res = r.post(url, credentials)
  res.raise_for_status()
  token = get_csrf(res)
  vprint("Successfully logged in!")
  return ((res.cookies, token))

# Extracts list of newly subscribed from confirmation page
def get_subscribed(pg):
  new_subs = []
  subs_list = pg.ul.li.text.split('\n')
  for sub in subs_list:
    if sub and 'Already a member' not in sub:
      new_subs.append(sub)
  if new_subs:
    vprint("List of new subscribers: " + str(new_subs))
  else:
    vprint("No new subscribers added.")
  return(new_subs)

def subscribe(domain, mailinglist, cookie, token, members_list):
  global sub_config
  url = 'http://lists.' + domain + '/cgi-bin/mailman/admin/' + mailinglist + '/members/add'
  sub_config['csrf_token'] = token
  res = r.post(url, cookies=cookie, data=sub_config, files=members_list)
  res.raise_for_status()
  vprint("Successfully subscribed!")
  return get_subscribed(bs(res.text, 'html.parser'))

# Extracts the csrf_token from html page
def get_csrf(sub_page):
  html = bs(sub_page.text, 'html.parser')
  token = html.input['value']
  return (token)

def logout(domain, mailinglist, cookie):
  url = 'http://lists.' + domain + '/cgi-bin/mailman/admin/' + mailinglist + '/logout'
  r.get(url, cookie).raise_for_status()
  vprint("Successfully logged out!")
  return (0)

def main(domain, mailinglist, password, members_file):
  members_list = { 'subscribees_upload': open(members_file, 'rb')}
  (session_cookie, csrf_token) = login(domain, mailinglist, password)
  subscribe(domain, mailinglist, session_cookie, csrf_token, members_list)
  logout(domain, mailinglist, session_cookie)
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

