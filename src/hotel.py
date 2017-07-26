
class Hotel(object):
	def __init__(self, id, amenities):
		print 'amenities', amenities
		self.id = id
		self.has_wifi = 'wifi' in str(amenities)
		self.has_spa = 'spa' in amenities
		self.has_restaurant = 'restaurant' in amenities
		self.has_fitness = 'fitness_room' in amenities
		self.has_car = 'airport_shuttle' in amenities
		self.has_cleaning = 'cleaning_products' in amenities
		self.has_attractions = 'attractions' in amenities
		self.has_pool = 'pool' in str(amenities)
		self.has_view = 'view' in str(amenities)
		self.has_beach = 'beach' in str(amenities)

	def get_amenities(self):
		amenities = []
		if self.has_wifi:
			amenities.append('has_wifi')
		if self.has_spa:
			amenities.append('has_spa')
		if self.has_restaurant:
			amenities.append('has_restaurant')
		if self.has_fitness:
			amenities.append('has_fitness')
		if self.has_car:
			amenities.append('has_car')
		if self.has_cleaning:
			amenities.append('has_cleaning')
		if self.has_attractions:
			amenities.append('has_attractions')
		if self.has_pool:
			amenities.append('has_pool')
		return amenities
		# return {
		# 	'has_wifi': self.has_wifi,
		# 	'has_spa': self.has_spa,
		# 	'has_restaurant': self.has_restaurant,
		# 	'has_fitness': self.has_fitness,
		# 	'has_car': self.has_car,
		# 	'has_cleaning': self.has_cleaning,
		# 	'has_attractions': self.has_attractions,
		# 	'has_pool': self.has_pool,
		# }


# 		hotel_url https://www.booking.com/hotel/nl/zandberg-canal-view-apartments.en.html?aid=881855&checkin=2017-11-28&checkout=2017-11-30&room1=A%2CA&room2=A&room3=A
# hotel_currency_code EUR
# photo http://aff.bstatic.com/images/hotel/max500_watermarked_standard_bluecom/2a7/2a7b411ae5044c069eed4ec5872e61e16a217cf5.jpg
# review_nr 0
# hotel_amenities [u'internet_services', u'wireless_lan', u'free_wifi_internet_access_included', u'all_public_and_private_spaces_non_smoking']
# checkin_time {u'from': u'14:00', u'until': u'00:00'}
# deep_link_url booking://hotel/2567915?checkout=2017-11-30&checkin=2017-11-28&affiliate_id=881855
# price 876.00
# group_rooms [{u'roomtype_id': u'5', u'breakfast_included': 0, u'adults': 2, u'all_inclusive': 0, u'full_board': 0, u'price': u'438.00', u'room_name': u'Deluxe King Suite', u'block_id': u'256791501_104317146_2_0_0', u'breakfast_cost': 0, u'deposit_required': 0, u'room_id': u'256791501', u'extra_charge': [{u'name': u'VAT', u'amount': u'24.79', u'charge_price_mode': u'percentage', u'excluded': 0, u'charge_amount': u'6.00', u'type': u'VAT'}, {u'name': u'City tax', u'amount': u'20.66', u'charge_price_mode': u'percentage', u'excluded': 1, u'charge_amount': u'5.00', u'type': u'CITYTAX'}], u'room_amenities': [u'coffee_tea_maker', u'shower', u'safe_deposit_box', u'hair_dryer', u'clothing_iron', u'seating_area', u'free_toiletries', u'patio', u'heating', u'satellite_channels', u'flat_screen_tv', u'electric_kettle', u'wardrobe_closet', u'lake_view', u'city_view', u'towels', u'linen', u'toilet_paper'], u'refundable': 1, u'refundable_until': u'2017-11-13 23:59:59 +0100', u'half_board': 0, u'children': [], u'num_rooms_available_at_this_price': 1}, {u'roomtype_id': u'5', u'breakfast_included': 0, u'adults': 2, u'all_inclusive': 0, u'full_board': 0, u'price': u'438.00', u'room_name': u'Deluxe King Suite', u'block_id': u'256791502_104317146_2_0_0', u'breakfast_cost': 0, u'deposit_required': 0, u'room_id': u'256791502', u'extra_charge': [{u'name': u'VAT', u'amount': u'24.79', u'charge_price_mode': u'percentage', u'excluded': 0, u'charge_amount': u'6.00', u'type': u'VAT'}, {u'name': u'City tax', u'amount': u'20.66', u'charge_price_mode': u'percentage', u'excluded': 1, u'charge_amount': u'5.00', u'type': u'CITYTAX'}], u'room_amenities': [], u'refundable': 1, u'refundable_until': u'2017-11-13 23:59:59 +0100', u'half_board': 0, u'children': [], u'num_rooms_available_at_this_price': 1}]
# default_language en
# hotel_id 2567915
# country nl
# cvc_required 0
# location {u'latitude': 52.3688637, u'longitude': 4.88714920000007}
# address Herengracht 367, Amsterdam City Centre, Amsterdam
# cc_required 1
# hotel_name Zandberg - Canal view apartments
# postcode 1016 BB