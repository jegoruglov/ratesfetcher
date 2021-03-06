RatesFetcher
============
is a cronjob that fetches exchange rates
with frequecies specified in configuration file.

Run from ratesfetcher directory
	
    ``python main.py``

To perform unit testing, run (ex.)

    ``python -m unittest test_rateparser``

or use Nose framework for batch testing
	
Rates source: ``http://www.ecb.int/home/html/rss.en.html``

Rates update frequency of source: daily

Rates update frequescy of fetcher: configurable


Features
--------
- Fetches 5 exchange rates concurrently
- Fetch rate for each exchange rate is configurable
- HTTP connection has configurable number of retries in case of failure
- Output options can be standard output, database, or both
- Test cases are created for linkparser, rateparser and ratefetcherthread
- Provides simple rates monitoring web server, based on Tornado web server and Highcharts javascript plotting library

Pre-set test environment
------------------------
- The ratesfetcher is launched for testing on 31.222.141.10
- To see charts visit ``http://31.222.141.10:8787/``
- To see all fetched currencies visit ``http://31.222.141.10:8787/exchange-rates``
- To see data for specific currency visit ``http://31.222.141.10:8787/rate-history/{currency}`` (ex. http://31.222.141.10:8787/rate-history/eek)
