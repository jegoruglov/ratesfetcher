import urllib2
import re
from ratesfetcher.config import conf

# Enables parsing html document based on xpath
# Requires third party module BeautifulSoup,
# hense not used in test version
#from BeautifulSoup import BeautifulSoup

class LinkParser(object):
	def __init__(self, uri, xpath=None, pattern=None):
		self.uri = uri
		self.xpath = xpath
		self.pattern = pattern

	def parse(self):
		try:
			html = urllib2.urlopen(self.uri).read()
		except HTTPError as e:
			# TODO: as the utility is a cronjob,
			# might want to log instead of raising
			raise e
		
		pattern = re.compile(r'<a[^>]*>')
		a_tags = pattern.findall(html)
		pattern = re.compile(conf.links_pattern)
		links = {}
		for tag in a_tags:
			m = pattern.search(tag)
			if m is not None:
				links[m.groups()[1]] = conf.rates_uri_base+m.groups()[0]
		return links