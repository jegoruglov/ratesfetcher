import os
import sys
import sqlite3
import json
sys.path.append("/home/jegor/projects/tornado")

import tornado.ioloop
import tornado.web

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static")
}

class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.db = sqlite3.connect('../ratesfetcher.db')
        self.c = self.db.cursor()
    def get(self):
        self.c.execute(
            'select name from sqlite_master where type = "table"')
        tables = [i[0] for i in self.c.fetchall()]
        self.render("main.html", tables=tables)

class ExchangeRatesHandler(MainHandler):
    def get(self):
        self.c.execute(
            'select name from sqlite_master where type = "table"')
        tables = [i[0] for i in self.c.fetchall()]
        self.write(json.dumps(tables))

class RateHistoryHandler(MainHandler):
    def get(self, rate):
        self.c.execute('select timestamp, rate from {0}'.format(rate))
        rates = [[i[0]*1000, i[1]] for i in self.c.fetchall()]
        self.write(json.dumps(
            {
                'name': rate,
                'data': rates
            }
        ))

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/exchange-rates", ExchangeRatesHandler),
    (r"/rate-history/([a-zA-Z]{3})", RateHistoryHandler)
], **settings)

if __name__ == "__main__":
    application.listen(8787)
    tornado.ioloop.IOLoop.instance().start()