# config
DB = {'host': '127.0.0.1',
	  'user': 'root',
	  'pw': '',
	  'database': 'group_trip'
	  }

DB_STRING = "mysql://{}:{}@{}/{}".format(DB['user'], DB['pw'], DB['host'], DB['database'])
