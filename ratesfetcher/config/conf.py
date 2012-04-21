# The source of rate links
rates_source_uri = "http://www.ecb.int/home/html/rss.en.html"
# The pattern to search for rss link, specific to the source page
links_pattern = r'''href=['"](/rss/fxref-([a-z]{3})\.html)['"]'''
# If DOM parser is used (ex. BeautifulSoup), use xpath to navigate
links_xpath = None

# If rate links are relative, specify the uri base
rates_uri_base = "http://www.ecb.int"
# The pattern to search exchange rate float number, specific to cource
rate_pattern = r'<cb:value[^>]*>([^<]*)</cb:value>'

# Update rate for rss links
links_update_rate = 60 * 60 * 24 # seconds

# Number of threads per fetch
number_of_threads = 5

# Update rate can be common for all exchange rates
common_update_rate = 30 # seconds
# or specific to each exchange rate
rateswise_update_rate = {
	'aud': 10, # seconds
	'bgn': 10,
	'brl': 10,
	'cad': 10,
	'chf': 10,
	'cny': 10,
	'czk': 10,
	'dkk': 10,
	'eek': 10,
	'gbp': 10,
	'hkd': 30,
	'hrk': 30,
	'huf': 30,
	'idr': 30,
	'inr': 30,
	'jpy': 30,
	'krw': 30,
	'ltl': 30,
	'lvl': 30,
	'mxn': 30,
	'myr': 60,
	'nok': 60,
	'nzd': 60,
	'php': 60,
	'pln': 60,
	'ron': 60,
	'rub': 60,
	'sek': 60,
	'sgd': 60,
	'thb': 60,
	'try': 60,
	'usd': 60,
	'zar': 60
}
# Select update strategy
#update_according_to = 'common_update_rate'
update_according_to = 'rateswise_update_rate'

# SQLite storage file name (relative or absolute path)
database_file = 'ratesfetcher.db'
# Comma-separated output options
#	std: standard output
#	db: SQLite database
output_options = 'db'

# Connection retries
number_of_connection_retries = 5