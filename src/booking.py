# booking.com api stuff here
import datetime
import json
import os

import requests
from requests.auth import HTTPBasicAuth

BOOKING_URL = "https://distribution-xml.booking.com/json"
USER = os.environ.get('BOOKING_USER')
PW = os.environ.get('BOOKING_PW')

class BookingAPI(object):
    def __init__(self):
        self.auth = HTTPBasicAuth(USER, PW)

    def _get_data(self, endpoint, params=None):
        try:
            url = "{}{}".format(BOOKING_URL, endpoint)
            print 'url', url
            params = params or {}
            print 'params', params
            r = requests.get(url, params=params, auth=self.auth)
            r.raise_for_status()
            return r.text
        except Exception as e:
            print 'problem!', e
            return {}

    def get_hotel_types(self):
        endpoint = '/getHotelTypes'
        params = {'languagecodes': ['en']}
        return json.loads(self._get_data(endpoint, params))

    def get_hotels(self, city_id, hotel_type_ids, fields):
        endpoint = '/getHotels'
        params = {
            'city_ids': [city_id],
            'hotel_type_ids': hotel_type_ids,
            'fields': fields,
        }
        hotels = self._get_data(endpoint, params)
        return json.loads(hotels)


    def get_hotel_availability(self, checkin, checkout, min_price, max_price, room_arrangement, dest_type, dest_id):
        endpoint = '/getHotelAvailabilityV2'
        params = {
            'checkin': datetime.date(checkin.year, checkin.month, checkin.day),
            'checkout': datetime.date(checkout.year, checkout.month, checkout.day),
            'min_price': min_price,
            'max_price': max_price,
            'output': 'hotel_details, hotel_amenities, room_details, room_amenities',
        }

        for room_num, room_occupancy in room_arrangement:
            params[room_num] = room_occupancy

        if dest_type == 'city':
            params['city_ids'] = [dest_id]
        # only cities for now...
        # elif dest_type == 'district':
            # params['city_ids'] = [dest_type]

        available_hotels = self._get_data(endpoint, params)
        return json.loads(available_hotels)



if __name__ == "__main__":
    b = BookingAPI()
    # params = {
    #     'checkin': '2017-12-10',
    #     'checkout': '2017-12-12',
    #     'room1': 'A,A',
    #     'output': 'hotel_details, hotel_amenities, room_details, room_amenities',
    #     'city_ids': [-824931,-929030],
    #     # 'hotel_ids': [472820],

    # }
    # data = b._get_data('/getHotelAvailabilityV2', params)
    # print 'data', data
