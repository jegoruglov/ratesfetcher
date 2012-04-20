import threading
import time
from Queue import Queue

from ratesfetcher.models import fetcherdatastore
from ratesfetcher.models import ratefetcherthread
from ratesfetcher.models import linkparser
from ratesfetcher.config import conf

class Fetcher(object):
	def __init__(self, output='std'):
		self.links_parser = linkparser.LinkParser(
			conf.rates_source_uri, pattern=conf.links_pattern
		)
		self.links = self.links_parser.parse()
		self.links_update_countdown = conf.links_update_rate
		self.rates_update_countdown = 1
		self.q = Queue(conf.number_of_threads)
		self.output = output

	def fetch(self):
		while True:
			# Update links if time has come
			if self.links_update_countdown == 0:
				self.__init__()
			# Make a list of exchange rates that are ready for update
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
				timestamp = time.ctime()
				output = [s.strip() for s in self.output.split(',')]
				if 'std' in output:
					for result in results:
						print timestamp, result
					print
				if 'db' in output:
					db = None
					try:
						db = fetcherdatastore.FetcherDataStore(
							conf.database_file)
					except:
						raise Exception('Database connection error')
					for result in results:
						if result['rate'] and result['name']:
							db.insert(result['name'], timestamp, result['rate'])
					if db:
						db.close()

			self.links_update_countdown -= 1
			self.rates_update_countdown += 1
			time.sleep(1)
