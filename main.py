from controllers import fetcher

def fetch():
	f = fetcher.Fetcher(output='std,db')
	f.fetch()

if __name__ == "__main__":
    fetch()
