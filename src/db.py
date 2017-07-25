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


    def insert(self, query):
        conn = self.get_conn()
        conn.execute(query)
        conn.close()

    def store_vote_result(self, email, location, start_date, end_date, price_min, price_max, has_car=None, has_cleaning=None,
                          has_fitness=None, has_wifi=None, has_attractions=None, has_restaurant=None, has_spa=None, has_pool=None,
                          has_view=None, is_hotel=None, is_bnb=None, is_villa=None, is_apt=None, is_campsite=None, is_resort=None):
        # query = 
        pass

    def create_group_trip(self, organizer_id, trip_title, **kwargs):
        query = "INSERT INTO trip (user_id, trip_title,".format(organizer_id)
        values = ' VALUES ({}, "{}",'.format(organizer_id, trip_title)

        for k, v in kwargs.iteritems():
            query += ' {},'.format(k)
            if type(v) is str:
                values += ' "{}",'.format(v)
            else:
                values += ' {},'.format(v)
        query = query[:-1]
        values = values[:-1]
        query += ')'
        values += ')'
        query += values

        self.insert(query)
        return True


if __name__ == "__main__":
    trip_db = TripDB()
    params = {'location': 123, 'min_price': 300, 'max_price': 600, 'message': 'come with me'}
    print params.keys()
    print params.values()
    trip_db.create_group_trip(6, 'my cool trip', **params)
    # conn = trip_db.get_conn()
    # conn.execute("INSERT INTO trip (user_id) VALUES (5)")
    # conn.close()




