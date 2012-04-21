import unittest
import re

import __init__
from ratesfetcher.models import ratefetcherthread

class RateFetcherThreadTest(unittest.TestCase):
	def setUp(self):
		self.link = {
			"name": "gbp",
			"uri": "http://www.ecb.int/rss/fxref-gbp.html"	
		}

	def test_fetch_rate(self):
		rate_fetcher_thread = ratefetcherthread.RateFetcherThread(self.link)
		rate_fetcher_thread.start()
		rate_fetcher_thread.join()
		result = rate_fetcher_thread.get_result()
		self.assertIsInstance(result, dict,
			'Rate must be of type dict')
		self.assertEqual(len(result), 2,
			'Rate dict must contain exactly two fields')
		self.assertIn('name', result, 
			'Rate dict must contain currency name')
		self.assertIn('rate', result,
			'Rate dict must contain exchange rate')
		self.assertTrue(re.match(r'[a-zA-Z]*', result['name']),
			'Currency name string must contain letters only')
		self.assertTrue(re.match(r'.{3}', result['name']),
			'Currency name string must be 3 characters long')
		self.assertIsInstance(result['rate'], float,
			'Exchange rate must be of type float')
		