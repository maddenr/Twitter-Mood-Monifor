import sqlite3
class SQLDBConnector:

# Constructor
#
	def __init__(self):
		self.db = self.__openDB__() #default db name
		cursor = self.db.cursor()
		
		cursor.execute("CREATE TABLE IF NOT EXISTS lotcation_mood_data(location TEXT PRIMARY KEY, total_parsed INTEGER,num_happy INTEGER, num_unhappy INTEGER)")
		cursor.execute("CREATE TABLE IF NOT EXISTS sample_tweets(tweet_id INTEGER PRIMARY KEY, location TEXT, text TEXT,num_happy INTEGER, num_unhappy INTEGER)")
		self.db.commit()
		cursor.close()
	
# Creates a transactional query on the DB
#In:		sql syntax
#Out:	List of results
	def __queryDB__(self, syntax):
		cur = self.db.cursor()
		cur.execute(syntax)
		results = cur.fetchall()
		cur.close()
		self.db.commit()
		
		return results

# Safely open a DB connection
#In:		None
#Out:	sqlite.Connection Object
	def __openDB__(self):
		return sqlite3.connect("MoodMonitor")

		
# Safely close the db connection
#In:		None
#Out:	None
	def __closeDB__(self):
		self.db.close() 
	
# builds insert all syntax and executes it against the db
#In:		tablename and list od data tuples
#Out:	boolean value based on success
	def insertAll(self, tableName, dataList):
	# determine the boilerplate syntax
		if tableName == "location_mood_data":
			sqliteInsertAllSyntax = "INSERT OR IGNORE INTO "+tableName+" ('location', 'total_parsed', 'num_happy', 'num_unhappy') VALUES "
		elif tableName == "sample_tweets":
			sqliteInsertAllSyntax = "INSERT OR IGNORE INTO "+tableName+" ('tweet_id', 'location', 'text', 'num_happy', 'num_unhappy') VALUES "
		else:
			assert True is False #trigger an error if it's a bad tableName
		
	# build the records to be inserted based on the types of values
		valuesSyntax = ""
		for dataTuple in dataList:
			valuesSyntax +="("
			for field in dataTuple:
				if type(field) is str:
					valuesSyntax += "'"+field+"',"
				elif type(field) is int:
					valuesSyntax += str(field)+","
				elif type(field) is tuple:
					valuesSyntax += str(field[0])+","+str(field[1])+","
			valuesSyntax = valuesSyntax[:-1]+")," #eliminate last comma and close the parens
			
		#print repr(sqliteInsertAllSyntax+valuesSyntax[:-1]+";")	#used in testing
		results = self.__queryDB__(sqliteInsertAllSyntax+valuesSyntax[:-1]+";") #eliminate the last comma and close query with ;
		#parse results to determine the return type
		return False

# used in testing
	def test(self, tableName):
			print self.__queryDB__("SELECT * FROM "+tableName)
			
			
			
			
			