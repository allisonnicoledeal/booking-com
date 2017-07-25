# booking.com api stuff here
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

    def get_hotels(self, city_id, hotel_type_id):
        endpoint = '/bookings.getHotels'
        params = {
            'city_ids': [city_id],
            'hotel_type_ids': [hotel_type_id],
        }
        hotels = self._get_data(endpoint, params)
        return hotels

    def get_available_hotels(self, checkin, checkout, num_adults, dest_id, dest_type, property_types, min_price, max_price):
        # get hotels for the city, assume all dest types are city for mvp
        print 'property_types', property_types
        # area_hotels = get_hotels(dest_id, )
        return




        # get the availabilities for those hotels


        endpoint = '/bookings.getHotelAvailabilityV2'
        params = {
            'checkin': checkin,
            'checkout': checkout,
            'min_price': min_price,
            'max_price': max_price,
            'property_type': property_type

        }

        if dest_type == 'city':
            params['city_ids'] = [dest_id]
        elif dest_type == 'district':
            params['city_ids'] = [dest_type]

        params['output'] = 'hotel_details, hotel_amenities, room_details, room_amenities'


        print 'endpoint', endpoint
        # params['landmark_ids'] = 701
        # params['latitude'] = 4.8952
        # params['hotel_ids'] = [11024]
        # params['region_ids'] = [10808]
        # params['longitute'] = 57.3702
        params['room1'] = 'A,A'

        print 'params', params



        data = self._get_data(endpoint, params)
        return data



if __name__ == "__main__":
    import json
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




    # print b.get_hotels(-824931, 5)


    # endpoint = '/getFacilityTypes'
    # data = b._get_data(endpoint,)
    # print data


    # r = requests.get('https://distribution-xml.booking.com/json/getHotelAvailabilityV2?checkin=2017-12-10&checkout=2017-12-12-&room1=A,A&output=room_details,hotel_details&hotel_ids=11223344')
    # print 'resp', r
    # endpoint = '/bookings.autocomplete'
    # params = {
    #     'text': 'Amsterdam',
    #     'languagecode': 'en'
    # }
    # autocomplete_res = b._get_data(endpoint, params)
    # for res in json.loads(autocomplete_res):
    #     print res
    #     print ''

    # for k,v in json.loads(autocomplete_res)[0].iteritems():
    #     print k, v

    # city_id = 


    # endpoint = '/bookings.getCities'
    # params = {'rows': 10}
    # # # params = {}

    #     # url = 'https://distribution-xml.booking.com/json/getHotelAvailabilityV2?
    #     # checkin={}
    #     # checkout={}
    #     # room1=A,A
    #     # output=room_details,hotel_details
    #     # hotel_ids={}'.format(checkin, checkout,  hotel_id)



    # data = b.get_available_hotels('2017-12-02', '2017-12-05', 5, 'hostel', -824931, 'city', min_price=300, max_price=1000)
    # print data
