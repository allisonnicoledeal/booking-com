# do calculations here
from collections import defaultdict
import operator

import booking
import db


trip_db = db.TripDB()
booking_api = booking.BookingAPI()

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


def process_voting_date():
	pass



def get_best_hotels(trip_id, limit):
	trip_votes_data = trip_db.get_trip_votes(trip_id)
	trip_data = trip_db.get_trip_info(trip_id)
	print 'trip_data', trip_data
	# print trip_votes_data

	vote_tallies = defaultdict(int)
	min_budgets = []
	max_budgets = []
	hotel_types = set()
	dest_ids = defaultdict(int)
	dates = defaultdict(int)

	for vote in trip_votes_data:
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
				vote_tallies[option] += 1

				if option in ACCOMMODATION_MAPPING:
					hotel_types.add(ACCOMMODATION_MAPPING[option])

	min_budget_median = get_median(min_budgets)
	max_budget_median = get_median(max_budgets)
	print 'min_budget_median', min_budget_median
	print 'max_budget_median', max_budget_median

	min_price = min_budget_median * trip_data['num_persons']
	max_price = max_budget_median * trip_data['num_persons']


	best_dates = sorted(dates.items(), key=operator.itemgetter(1), reverse=True)
	hightest_match = best_dates[0]


	print best_dates[0]

	# sorted_preferences = sorted(vote_tallies.items(), key=operator.itemgetter(1), reverse=True)
	# print sorted_preferences
	print vote_tallies

	print 'hotel_types', hotel_types

	# hotel_types = booking_api.get_hotel_types()
	# print 'hotel_types', hotel_types
	# hotel_type = ACCOMMODATION_MAPPING[]


	# hotels = booking_api.get_available_hotels(vote_tallies['start_date'], vote_tallies['end_date'], hotel_types, min_price, max_price)


if __name__ == "__main__":
	get_best_hotels(5, 10)

