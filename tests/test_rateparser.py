import unittest

import __init__
from ratesfetcher.models import rateparser

class RateParserTest(unittest.TestCase):
	def setUp(self):
		self.uri = 'http://www.ecb.int/rss/fxref-gbp.html'

	def test_parse(self):
		rate_parser = rateparser.RateParser(self.uri)
		rate = rate_parser.parse()
		self.assertIsInstance(rate, float,
			'rate has to be of type float')