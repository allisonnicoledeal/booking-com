from flask import Flask

import calc
import db
import emails

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Rebellama'

# @app.route('/getGroupTrip', methods=['GET']))
# def grogetGroupTripupTrip():
    # return 'Rebellama'

@app.route('/createGroupTrip', methods=['POST'])
def createGroupTrip(trip_title, emails):
    # store data into db here
    # send emails
    return 'Rebellama'

@app.route('/getVotingPage', methods=['GET'])
def getVotingPage():
    return 'Rebellama'

@app.route('/submitVote', methods=['POST'])
def submitVote(email, location, start_date, end_date, price_min, price_max, has_car=None, has_cleaning=None, has_fitness=None,
               has_wifi=None, has_attractions=None, has_restaurant=None, has_spa=None, has_pool=None, has_view=None,
               is_hotel=None, is_bnb=None, is_villa=None, is_apt=None, is_campsite=None, is_resort=None):
    # store to trip details db
    db.store_vote_result(email, location, start_date, end_date, price_min, price_max, has_car=None, has_cleaning=None,
                         has_fitness=None, has_wifi=None, has_attractions=None, has_restaurant=None, has_spa=None, has_pool=None,
                         has_view=None, is_hotel=None, is_bnb=None, is_villa=None, is_apt=None, is_campsite=None, is_resort=None)
    return 'Rebellama'

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