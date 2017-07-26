# do calculations here
from collections import defaultdict
import math
import operator

import booking
import db
from hotel import Hotel


ACCOMMODATION_MAPPING = {
    'is_hotel': 'Hotel',
    'is_bnb': 'Bed and Breakfast',
    'is_villa': 'Residence',
    'is_apt': 'Apartment',
    'is_resort': 'Resort',
}

def get_median(lst):
    lst = sorted(lst)
    n = len(lst)
    if n < 1:
        return None
    if n % 2 == 1:
        return lst[n//2]
    else:
        return sum(lst[n//2-1:n//2+1])/2.0


class BestHotelAnalyzer(object):
    def __init__(self, trip_id, limit):
        self.trip_db = db.TripDB()
        self.booking_api = booking.BookingAPI()

        self.trip_votes_data = self.trip_db.get_trip_votes(trip_id)
        self.trip_data = self.trip_db.get_trip_info(trip_id)

        self.best_start = None
        self.best_end = None
        self.num_guests = self.trip_data['num_persons']
        self.best_dest_id = None
        self.best_dest_type = None
        self.hotel_type_infos = []
        self.min_price = None
        self.max_price = None
        self.room_arrangement = []

        self.data_setup()


    def data_setup(self):
        self.vote_tallies = defaultdict(int)
        min_budgets = []
        max_budgets = []
        hotel_types = set()
        dest_ids = defaultdict(int)
        dates = defaultdict(int)

        for vote in self.trip_votes_data:
            min_budget = vote.pop('min_budget', None)
            if min_budget:
                min_budgets.append(int(min_budget))

            max_budget = vote.pop('max_budget', None)
            if max_budget:
                max_budgets.append(int(max_budget))

            dest_id = vote.pop('dest_id', None)
            dest_type = vote.pop('dest_type', None)
            if dest_id and dest_type:
                dest_ids[(dest_id, dest_type)] += 1

            start_date = vote.pop('start_date', None)
            end_date = vote.pop('end_date', None)
            if start_date and end_date:
                dates[(start_date, end_date)] += 1


            for option, answer in vote.iteritems():
                if answer:
                    self.vote_tallies[option] += 1

                    if option in ACCOMMODATION_MAPPING:
                        hotel_types.add(ACCOMMODATION_MAPPING[option])

        # budget
        min_budget_median = get_median(min_budgets)
        max_budget_median = get_median(max_budgets)
        self.min_price = min_budget_median
        # self.min_price = min_budget_median * self.num_guests
        self.max_price = max_budget_median
        # self.max_price = max_budget_median * self.num_guests

        # dates
        best_dates = sorted(dates.items(), key=operator.itemgetter(1), reverse=True)[0]
        # best_dates = [dates for dates in best_dates if dates[1] == best_dates[0][1]]
        self.best_start = best_dates[0][0]
        self.best_end = best_dates[0][1]

        # locations
        best_location = sorted(dest_ids.items(), key=operator.itemgetter(1), reverse=True)[0]
        self.best_dest_id = best_location[0][0]
        self.best_dest_type = best_location[0][1]

        all_type_info = self.booking_api.get_hotel_types()

        # hotel type names & ids
        for hotel_type in hotel_types:
            for type_info in all_type_info:
                if type_info['name'] == hotel_type:
                    self.hotel_type_infos.append((hotel_type, type_info['hoteltype_id']))

        # room arrangements
        num_solo_rooms = self.vote_tallies.get('solo_room', 0)
        num_rooms = int(math.ceil(float(self.num_guests) / 2)) + (num_solo_rooms / 2)
        for idx in range(1, num_rooms+1):
            if idx <= num_solo_rooms:
                self.room_arrangement.append(("room{}".format(idx), 'A,A'))
            else:
                self.room_arrangement.append(("room{}".format(idx), 'A'))


    def get_matching_hotels(self):
        # get hotels for the city, assume all dest types are city for mvp
        property_type_ids = [type_id for type_name, type_id in self.hotel_type_infos]
        area_hotels = self.booking_api.get_hotels(self.best_dest_id, property_type_ids,
                                                  ['hotel_id', 'max_rooms_in_reservation', 'max_persons_in_reservation'])

        potential_hotels = []
        for h in area_hotels:
            max_rooms = int(h['max_rooms_in_reservation'])
            max_persons = int(h['max_persons_in_reservation'])
            if ((not max_rooms or max_rooms >= len(self.room_arrangement)) and 
                (not max_persons or max_persons >= self.num_guests)):
                potential_hotels.append(h['hotel_id'])

        # get the availabilities for those hotels
        property_type_names = [type_name for type_name, type_id in self.hotel_type_infos]
        hotel_availability = self.booking_api.get_hotel_availability(self.best_start, self.best_end, self.min_price, self.max_price,
                                                                     self.room_arrangement, self.best_dest_type, self.best_dest_id)
        hotels_info = hotel_availability['hotels']

        hotels_to_compare = []
        for h in hotels_info:
            hotels_to_compare.append(Hotel(h['hotel_id'], h['hotel_amenities']))
        return hotels_to_compare


    def find_optimal_hotel(self):
        # if there is one best date & location, great!
        # if there are ties, we need to address tie breakers in next version
        hotels = self.get_matching_hotels()
        best_hotel = None
        best_score = -1
        for hotel in hotels:
            amenities = hotel.get_amenities()
            hotel_score = 0
            for vote_item, score in self.vote_tallies.iteritems():
                if vote_item in amenities:
                    hotel_score += score

            if hotel_score > best_score:
                best_hotel = hotel.id
                best_score = hotel_score
        return best_hotel


if __name__ == "__main__":
    analyzer = BestHotelAnalyzer(5, 10)
    analyzer.find_optimal_hotel()

