import urllib2
import re

from ratesfetcher.config import conf

# Normally I'd use third party package feedparser,
# but will keep less dependencies for test version.
#import feedparser

class RateParser(object):
	def __init__(self, uri):
		self.uri = uri

	def parse(self):
		retry_counter = conf.number_of_connection_retries
		xml = None
		while retry_counter:
			try:
				xml = urllib2.urlopen(self.uri).read()
				if xml:
					break
			except urllib2.HTTPError:
				print "ERROR: HTTP connection failed, retrying ..."
				retry_counter -= 1

		if not xml:
			raise Exception('HTTP Error while fetching rates')
		
		pattern = re.compile(conf.rate_pattern)
		rates = pattern.findall(xml)
		assert rates, 'rates should not be empty'
		try:
			rate = float(rates[0])
		except ValueError as e:
			raise e
		return rate