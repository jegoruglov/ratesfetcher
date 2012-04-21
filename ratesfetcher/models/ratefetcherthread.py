import threading

from ratesfetcher.models import rateparser

class RateFetcherThread(threading.Thread):
	def __init__(self, link):
		threading.Thread.__init__(self)
		self.name = link['name']
		self.rate_parser = rateparser.RateParser(link['uri'])
		self.result = None
	
	def get_result(self):
		return {
			'name': self.name,
			'rate': self.result
		}

	def run(self):
		rate = self.rate_parser.parse()
		self.result = rate