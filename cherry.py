#!/usr/bin/env python

import os
import cherrypy
from nsetools import Nse
import redis
import json

#accesing nifty top 50 gainers list

nse = Nse()
top_gainers = nse.get_top_gainers()
r = redis.Redis(host='localhost', port=6379, db=0, password='yourpassword')
json_gainers = json.dumps(top_gainers)
r.set('top_gainers', json_gainers)
unpacked_gainers = json.loads(r.get('top_gainers'))
top_gainers == unpacked_gainers

class CherryNse(object):
    @cherrypy.expose
    def index(self):    
        index = open("index.html").read().format(top_gainers=top_gainers)
        return index

cherrypy.config.update({'server.socket_host': '0.0.0.0'})
if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.quickstart(CherryNse(), '/', conf)
