import urllib2
import re

from ratesfetcher.config import conf

# Enables parsing html document based on xpath
# Requires third party module BeautifulSoup,
# hense not used in test version, to avoid dependencies
#from BeautifulSoup import BeautifulSoup

class LinkParser(object):
	def __init__(self, uri, xpath=None, pattern=None):
		self.uri = uri
		self.xpath = xpath
		self.pattern = pattern

	def parse(self):
		retry_counter = conf.number_of_connection_retries
		html = None
		while retry_counter:
			try:
				html = urllib2.urlopen(self.uri).read()
				if html:
					break
			except urllib2.HTTPError:
				print "ERROR: HTTP connection failed, retrying ..."
				retry_counter -= 1

		if not html:
			raise Exception('HTTP Error while fetching rss links')
		
		pattern = re.compile(r'<a[^>]*>')
		a_tags = pattern.findall(html)
		pattern = re.compile(conf.links_pattern)
		links = {}
		for tag in a_tags:
			m = pattern.search(tag)
			if m is not None:
				links[m.groups()[1]] = conf.rates_uri_base+m.groups()[0]
		return links