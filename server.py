#!/usr/bin/env python
from flask import Flask, request
import json
import urllib2
from werkzeug.contrib.cache import SimpleCache

from jira.client import JIRA
from configuration import *

app = Flask(__name__)
cache = SimpleCache()

CACHE_TIMEOUT = 5*60

def auth_jira_url(url):
    return url + "&os_username=" + JIRA_USERNAME + "&os_password=" + JIRA_PASSWORD

####################################################################
# Routes
####################################################################

@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')

@app.route('/jira/today', methods=['GET'])
def jira_today():
    rv = cache.get('jira_today')
    if rv is None:
        rv = urllib2.urlopen(auth_jira_url(JIRA_BASE_URL + "/rest/api/2/search?jql=status=\"Do%20Today\"&fields=summary")).read()
        cache.set('jira_today', rv, timeout=CACHE_TIMEOUT)
        return rv
    else:
        return rv

@app.route('/jira/tomorrow', methods=['GET'])
def jira_tomorrow():
    rv = cache.get('jira_tomorrow')
    if rv is None:
        rv = urllib2.urlopen(auth_jira_url(JIRA_BASE_URL + "/rest/api/2/search?jql=\"Schedule%20Date\"=startOfDay(1d)%20OR%20status=\"Do%20Tomorrow\"&fields=summary")).read()
        cache.set('jira_tomorrow', rv, timeout=CACHE_TIMEOUT)
        return rv
    else:
        return rv

####################################################################
# Start Flask
####################################################################
if __name__ == '__main__':
    app.run(debug=True)