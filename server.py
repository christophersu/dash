#!/usr/bin/env python
from flask import Flask, request
import json
import urllib2
from werkzeug.contrib.cache import SimpleCache
import os

try:
    from configuration import *
except:
    JIRA_BASE_URL = os.environ['JIRA_BASE_URL']
    JIRA_USERNAME = os.environ['JIRA_USERNAME']
    JIRA_PASSWORD = os.environ['JIRA_PASSWORD']
    API_SECRET = os.environ['API_SECRET']

app = Flask(__name__)
cache = SimpleCache()

CACHE_TIMEOUT = 5*60

def auth_jira_url(url):
    return url + "&os_username=" + JIRA_USERNAME + "&os_password=" + JIRA_PASSWORD

def check_api_secret(attempt):
    if attempt == API_SECRET:
        return True
    else:
        return False

####################################################################
# Routes
####################################################################

@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')

@app.route('/jira/today', methods=['GET'])
def jira_today():
    if check_api_secret(request.args.get('secret')):
        rv = cache.get('jira_today')
        if rv is None:
            rv = urllib2.urlopen(auth_jira_url(JIRA_BASE_URL + "/rest/api/2/search?jql=status=\"Do%20Today\"&fields=summary")).read()
            cache.set('jira_today', rv, timeout=CACHE_TIMEOUT)
            return rv
        else:
            return rv
    else:
        return 'Incorrect API secret.'

@app.route('/jira/tomorrow', methods=['GET'])
def jira_tomorrow():
    if check_api_secret(request.args.get('secret')):
        rv = cache.get('jira_tomorrow')
        if rv is None:
            rv = urllib2.urlopen(auth_jira_url(JIRA_BASE_URL + "/rest/api/2/search?jql=\"Schedule%20Date\"=startOfDay(1d)%20OR%20status=\"Do%20Tomorrow\"&fields=summary")).read()
            cache.set('jira_tomorrow', rv, timeout=CACHE_TIMEOUT)
            return rv
        else:
            return rv
    else:
        return 'Incorrect API secret.'

@app.route('/request/get', methods=['GET'])
def jira_tomorrow():
    if check_api_secret(request.args.get('secret')):
        rv = urllib2.urlopen(request.args.get('url')).read()
        return rv
    else:
        return 'Incorrect API secret.'

####################################################################
# Start Flask
####################################################################
if __name__ == '__main__':
    app.run(debug=True)