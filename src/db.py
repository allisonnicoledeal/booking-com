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

    def store_vote_result(self, email, location, start_date, end_date, price_min, price_max, has_car=None, has_cleaning=None,
                          has_fitness=None, has_wifi=None, has_attractions=None, has_restaurant=None, has_spa=None, has_pool=None,
                          has_view=None, is_hotel=None, is_bnb=None, is_villa=None, is_apt=None, is_campsite=None, is_resort=None):
        # query = 
        pass


    def create_group_trip(self, organizer_id, trip_title, location_ids, **kwargs):
        trip_query = "INSERT INTO trip (user_id, trip_title,".format(organizer_id)
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

        for location_id in location_ids:
            location_query = "INSERT INTO trip_locations (trip_id, booking_city_id) VALUES ({}, {})".format(trip_id, location_id)
            self.insert(location_query)

        return True

    def get_trip_info(self, trip_id):
        query = "SELECT * FROM trip WHERE id = {}".format(trip_id)
        return self.fetchone(query)


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




