#!/bin/python
# LICENSE: Apache License 2.0
# https://www.apache.org/licenses/LICENSE-2.0
#
# This is a modified version of the quickstart example from
# https://developers.google.com/sheets/api/quickstart/python

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

VERBOSE = True

sheet = '1xMyKMv3ENeAuHTIKyiRJD5gU8jJtr0D0y9Xd26gFCPg'
emailColumn = 'Members!C2:C'

def vprint(string):
  if VERBOSE:
    print(string)

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets email-list downloader'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
  credentials = get_credentials()
  http = credentials.authorize(httplib2.Http())
  discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                  'version=v4')
  service = discovery.build('sheets', 'v4', http=http,
                            discoveryServiceUrl=discoveryUrl)

  spreadsheetId = sheet
  rangeName = emailColumn
  result = service.spreadsheets().values().get(
      spreadsheetId=spreadsheetId, range=rangeName).execute()
  values = result.get('values', [])

  if not values:
    print('No data found.')
  else:
    print('email:')
    with open('members.txt', 'w') as f:
      for row in values:
        f.write(row[0] + '\n')
        vprint(row[0])


if __name__ == '__main__':
    main()

