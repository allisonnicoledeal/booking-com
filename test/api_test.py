# Play around with the booking.com API
import os

import requests
from requests.auth import HTTPBasicAuth

BOOKING_URL = "https://distribution-xml.booking.com/json"
USER = os.environ.get('BOOKING_USER')
PW = os.environ.get('BOOKING_PW')

auth = HTTPBasicAuth(USER, PW)

endpoint = '/bookings.getChains'
params = {'rows': 10}

print "Testing the booking.com url with the %s endpoint" % endpoint

r = requests.get("%s%s" % (BOOKING_URL, endpoint), params=params, auth=auth)
r.raise_for_status()
print r.text
