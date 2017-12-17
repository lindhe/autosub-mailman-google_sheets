# Auto subscriber for mailman

This program can download a list of email addresses from a Google Sheet and
update a mailman 2.1.20 database (on http, with the setup that chs.chalmers.se
uses) with those addresses.

## Dependencies

* python3
* python-requests
* python-beautifulsoup4
* google-api-python-client
