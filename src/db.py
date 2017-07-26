#db methods here
import sqlalchemy
# import MySQLdb

from cfg import DB_STRING


# db = sqlalchemy.create_engine(cfg.DB_STR, pool_recycle=600, pool_size=16)
class TripDB(object):

    def __init__(self):
        # self.conn = self.get_conn(DB['host'], user=DB['user'], passwd=DB['pw'], db=DB['database'])
        self.db_pool = sqlalchemy.create_engine(DB_STRING)

    def get_conn(self):
        return self.db_pool.connect()

    def fetchall(self, query):
        conn = self.get_conn()
        result = [dict(u) for u in conn.execute(query).fetchall()]
        conn.close()
        return result

    def fetchone(self, query):
        conn = self.get_conn()
        r = conn.execute(query).fetchone()
        result = None
        if r:
            result = dict(r)
        conn.close()
        return result


    def insert(self, query, return_id=False):
        # TODO: unsafe insert queries, fix this
        conn = self.get_conn()
        res = conn.execute(query)
        conn.close()
        return res.lastrowid

    def create_vote_result(self, trip_id, **kwargs):
        vote_query = "INSERT INTO trip_votes (trip_id,"
        values = ' VALUES ({},'.format(trip_id)

        for k, v in kwargs.iteritems():
            vote_query += ' {},'.format(k)
            if type(v) is str:
                values += ' "{}",'.format(v)
            else:
                values += ' {},'.format(v)
        vote_query = vote_query[:-1]
        values = values[:-1]
        vote_query += ')'
        values += ')'
        vote_query += values
        self.insert(vote_query, return_id=True)

    def create_group_trip(self, organizer_id, trip_title, location_ids, date_ranges, **kwargs):
        """
        :type organizer_id: int, booking.com user id of organizer_id
        :type trip_title: str
        :type location_ids: list[(dest_id, dest_type)]
        :type date_ranges: list[(min datetime, max datetime)]
        """

        trip_query = "INSERT INTO trip (user_id, trip_title,"
        values = ' VALUES ({}, "{}",'.format(organizer_id, trip_title)

        for k, v in kwargs.iteritems():
            trip_query += ' {},'.format(k)
            if type(v) is str:
                values += ' "{}",'.format(v)
            else:
                values += ' {},'.format(v)
        trip_query = trip_query[:-1]
        values = values[:-1]
        trip_query += ')'
        values += ')'
        trip_query += values
        trip_id = self.insert(trip_query, return_id=True)

        for dest_id, dest_type in location_ids:
            location_query = "INSERT INTO trip_locations (trip_id, dest_id, dest_type) VALUES ({}, {})".format(trip_id, dest_id, dest_type)
            self.insert(location_query)

        for start_date, end_date in date_ranges:
            dates_query = 'INSERT INTO trip_dates (trip_id, start_date, end_date) VALUES ({}, "{}", "{}")'.format(trip_id, start_date, end_date)
            self.insert(dates_query)

        return True

    def get_trip_info(self, trip_id):
        query = "SELECT * FROM trip WHERE id = {}".format(trip_id)
        return self.fetchone(query)

    def get_trip_votes(self, trip_id):
        query = """
            SELECT  trip_votes.has_beach, trip_votes.has_car, trip_votes.has_cleaning, trip_votes.has_fitness,
              trip_votes.has_wifi, trip_votes.has_attractions, trip_votes.has_restaurant, trip_votes.has_spa,
              trip_votes.has_pool, trip_votes.has_view, trip_votes.is_hotel, trip_votes.is_bnb, trip_votes.is_villa,
              trip_votes.is_apt, trip_votes.is_campsite, trip_votes.is_resort, trip_votes.solo_room, trip_votes.min_budget,
              trip_votes.max_budget, trip_locations.dest_id, trip_locations.dest_type, trip_dates.start_date, trip_dates.end_date
            FROM trip_votes
            JOIN trip_locations ON trip_votes.trip_id = trip_locations.trip_id
            JOIN trip_dates ON trip_votes.trip_id = trip_dates.trip_id
            WHERE trip_votes.trip_id = {}
            AND trip_votes.trip_dates_id = trip_dates.id
            AND trip_votes.trip_location_id = trip_locations.id
        """.format(trip_id)
        return self.fetchall(query)


if __name__ == "__main__":
    trip_db = TripDB()
    params = {'min_price': 300, 'max_price': 600, 'message': 'come with me'}
    print params.keys()
    print params.values()
    location_ids = [17, 19]
    trip_db.create_group_trip(6, 'my cool trip', location_ids, **params)
    # conn = trip_db.get_conn()
    # conn.execute("INSERT INTO trip (user_id) VALUES (5)")
    # conn.close()




