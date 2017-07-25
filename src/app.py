from flask import Flask
from flask.json import jsonify

import calc
import db
import emails

app = Flask(__name__)
trip_db = db.TripDB()


@app.route('/', methods=['GET'])
def home():
    return 'Rebellama'


# @app.route('/getGroupTrip', methods=['GET']))
# def grogetGroupTripupTrip():
    # return 'Rebellama'


@app.route('/createGroupTrip', methods=['POST'])
def createGroupTrip(organizer_id, trip_title, email_addresses, message, location_ids, date_ranges, **kwargs):
    if message:
        kwargs.update(message)
    kwargs['num_persons'] = len(email_addresses)
    trip_id = trip_db.create_group_trip(organizer_id, trip_title, location_ids, date_ranges, kwargs)
    for email_address in email_addresses:
        emails.send_email(email_address, message)
    return trip_id


@app.route('/getVotingPage/<int:trip_id>', methods=['GET'])
def getVotingPage(trip_id):
    trip_info = trip_db.get_trip_info(trip_id)
    return jsonify(trip_info)


@app.route('/submitVote', methods=['POST'])
def submitVote(trip_id, location, date_range, price_min, price_max, has_car=None, has_cleaning=None, has_fitness=None,
               has_wifi=None, has_attractions=None, has_restaurant=None, has_spa=None, has_pool=None, has_view=None,
               is_hotel=None, is_bnb=None, is_villa=None, is_apt=None, is_campsite=None, is_resort=None):
    # store to trip details db
    trip_db.create_vote_result(trip_id, location, start_date, end_date, price_min, price_max, has_car=None, has_cleaning=None,
                               has_fitness=None, has_wifi=None, has_attractions=None, has_restaurant=None, has_spa=None, has_pool=None,
                               has_view=None, is_hotel=None, is_bnb=None, is_villa=None, is_apt=None, is_campsite=None, is_resort=None)
    return True
    # return db.execute("INSERT INTO trip_votes (trip_id, email,location, start_date, end_date, price_min,price_max,has_car, has_cleaning,has_fitness,has_wifi, has_attractions, has_restaurant, has_spa, has_pool, has_view, is_hotel,is_bnb,is_villa, is_apt, is_campsite, is_resort ) VALUES (trip_id, email,location, start_date, end_date, price_min,price_max,has_car, has_cleaning,has_fitness,has_wifi, has_attractions, has_restaurant, has_spa, has_pool, has_view, is_hotel,is_bnb,is_villa, is_apt, is_campsite, is_resort ) ");


# this will be called by a cron job
# cron job will scan db for voting complete, but stats missing
@app.route('/getBestHotels', methods=['GET'])
def getBestHotels(trip_id, limit):
    # calculate best pct and find best hotels, store to db
    calc.get_best_hotels(trip_id, limit)
    # notify organizer
    emails.send_vote_results()
    return 'Rebellama'


@app.route('/bookRoom', methods=['POST'])
def bookRoom(limit):
    # mock this portion for now
    return 'Rebellama'


if __name__ == '__main__':
    app.debug = True
    app.run()