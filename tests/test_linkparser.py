import unittest2

import __init__
from ratesfetcher.models import linkparser
from ratesfetcher.config import conf

class LinkParserTest(unittest2.TestCase):
	def setUp(self):
		self.uri = conf.rates_source_uri
		self.link_pattern = conf.links_pattern

	def test_parse(self):
		link_parser = linkparser.LinkParser(
			self.uri, 
			pattern=self.link_pattern
		)
		links = link_parser.parse()
		self.assertIsInstance(links, dict,
			'links should be a list')
		self.assertNotEqual(len(links), 0,
			'links dict should not be empty')
		self.assertEqual(
			links, 
			{
				'ron': 'http://www.ecb.int/rss/fxref-ron.html', 
				'myr': 'http://www.ecb.int/rss/fxref-myr.html', 
				'inr': 'http://www.ecb.int/rss/fxref-inr.html', 
				'jpy': 'http://www.ecb.int/rss/fxref-jpy.html', 
				'czk': 'http://www.ecb.int/rss/fxref-czk.html', 
				'brl': 'http://www.ecb.int/rss/fxref-brl.html', 
				'sek': 'http://www.ecb.int/rss/fxref-sek.html', 
				'sgd': 'http://www.ecb.int/rss/fxref-sgd.html', 
				'usd': 'http://www.ecb.int/rss/fxref-usd.html', 
				'aud': 'http://www.ecb.int/rss/fxref-aud.html', 
				'chf': 'http://www.ecb.int/rss/fxref-chf.html', 
				'zar': 'http://www.ecb.int/rss/fxref-zar.html', 
				'cny': 'http://www.ecb.int/rss/fxref-cny.html', 
				'hrk': 'http://www.ecb.int/rss/fxref-hrk.html', 
				'huf': 'http://www.ecb.int/rss/fxref-huf.html', 
				'eek': 'http://www.ecb.int/rss/fxref-eek.html', 
				'nok': 'http://www.ecb.int/rss/fxref-nok.html', 
				'rub': 'http://www.ecb.int/rss/fxref-rub.html', 
				'mxn': 'http://www.ecb.int/rss/fxref-mxn.html', 
				'pln': 'http://www.ecb.int/rss/fxref-pln.html', 
				'php': 'http://www.ecb.int/rss/fxref-php.html', 
				'hkd': 'http://www.ecb.int/rss/fxref-hkd.html', 
				'idr': 'http://www.ecb.int/rss/fxref-idr.html', 
				'krw': 'http://www.ecb.int/rss/fxref-krw.html', 
				'bgn': 'http://www.ecb.int/rss/fxref-bgn.html', 
				'thb': 'http://www.ecb.int/rss/fxref-thb.html', 
				'try': 'http://www.ecb.int/rss/fxref-try.html', 
				'gbp': 'http://www.ecb.int/rss/fxref-gbp.html', 
				'nzd': 'http://www.ecb.int/rss/fxref-nzd.html', 
				'lvl': 'http://www.ecb.int/rss/fxref-lvl.html', 
				'ltl': 'http://www.ecb.int/rss/fxref-ltl.html', 
				'dkk': 'http://www.ecb.int/rss/fxref-dkk.html', 
				'cad': 'http://www.ecb.int/rss/fxref-cad.html'
			},
			'unexpected links'
		)