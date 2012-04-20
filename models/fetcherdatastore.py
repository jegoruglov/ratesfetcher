import sqlite3

class FetcherDataStore(object):
	def __init__(self, database):
		try:
			self.connection = sqlite3.connect(database)
		except:
			raise Exception('''Unable to connect to sqlite database,
				check that sqlite3 database is installed 
				on the local machine''')
		self.cursor = self.connection.cursor()

	def insert(self, table, timestamp, rate):
		command = '''CREATE TABLE {0} 
			(timestamp text, rate double)'''.format(table)
		try:
			self.cursor.execute(command)
		except sqlite3.OperationalError:
			pass
		command = '''INSERT INTO {0} VALUES 
			('{1}', {2})'''.format(table, timestamp, rate)
		print command
		self.cursor.execute(command)

	def close(self):
		self.connection.commit()
		self.cursor.close()