import urllib2
import re

from ratesfetcher.config import conf

# Normally I'd use third party package feedparser here,
# but will keep less dependencies for test version.
#import feedparser

class RateParser(object):
	def __init__(self, uri):
		self.uri = uri

	def parse(self):
		try:
			xml = urllib2.urlopen(self.uri).read()
		except urllib2.HTTPError as e:
			# TODO: as the utility is a cronjob,
			# might want to log instead of raising
			raise e
		
		pattern = re.compile(conf.rate_pattern)
		rates = pattern.findall(xml)
		assert rates, 'rates should not be empty'
		try:
			rate = float(rates[0])
		except ValueError as e:
			raise e
		return rate