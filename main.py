import sys
import time
import traceback

import fetcher
from ratesfetcher.config import conf

def fetch():
	f = fetcher.Fetcher(output=conf.output_options)
	f.fetch()

if __name__ == "__main__":
    fetch()