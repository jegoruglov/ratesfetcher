import threading
import time
from Queue import Queue

from ratesfetcher.models import fetcherdatastore
from ratesfetcher.models import ratefetcherthread
from ratesfetcher.models import linkparser
from ratesfetcher.config import conf

class Fetcher(object):
	def __init__(self, output='std'):
		self.initialize()
		self.rates_update_countdown = 1
		self.q = Queue(conf.number_of_threads)
		self.output = output

	def initialize(self):
		self.links_parser = linkparser.LinkParser(
			conf.rates_source_uri, pattern=conf.links_pattern
		)
		self.links = self.links_parser.parse()
		self.links_update_countdown = conf.links_update_rate

	def fetch(self):
		while True:
			try:
				# Update links if time has come
				if self.links_update_countdown == 0:
					self.initialize()
				# Make a list of exchange rates that are ready for update
				links = self._update_links_list()

				def producer(q, links):
					for link in links:
						thread = ratefetcherthread.RateFetcherThread(link)
						thread.start()
						q.put(thread, True)

				results = []
				def consumer(q, total_links):
					while len(results) < total_links:
						thread = q.get(True)
						thread.join()
						results.append(thread.get_result())

				prod_thread = threading.Thread(
					target=producer, args=(self.q, links))
				cons_thread = threading.Thread(
					target=consumer, args=(self.q, len(links)))
				prod_thread.start()
				cons_thread.start()
				prod_thread.join()
				cons_thread.join()

				if results:
					ctime = time.ctime()
					output = [s.strip() for s in self.output.split(',')]
					if 'std' in output:
						self._std_out(results, ctime)
					if 'db' in output:
						timestamp = time.mktime(time.strptime(ctime))
						self._db_out(results, ctime, timestamp)
						
		    except Exception as e:
		    	print time.ctime(), "ERROR", e
		    	traceback.print_exc(file=sys.stdout)

			self.links_update_countdown -= 1
			self.rates_update_countdown += 1
			time.sleep(1)

	def _std_out(self, results, ctime):
		for result in results:
			print ctime, result
		print

	def _db_out(self, results, ctime, timestamp):
		db = None
		try:
			db = fetcherdatastore.FetcherDataStore(
				conf.database_file)
		except:
			raise Exception('Database connection error')
		for result in results:
			if result['rate'] and result['name']:
				db.insert(result['name'], ctime,
				timestamp, result['rate'])
		if db:
			db.close()
			print ctime, 'Data successfully inserted in DB'
			print

	def _update_links_list(self):
		links = []
		for k, v in self.links.iteritems():
			update_rate = getattr(conf, conf.update_according_to)
			try:
				update_rate = (isinstance(update_rate, dict)
					and update_rate[k]
					or update_rate)
			except KeyError as e:
				raise e
			if self.rates_update_countdown % update_rate == 0:
				links.append({
					"name": k,
					"uri": v
				})
		return links