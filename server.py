#!/usr/bin/env python
from flask import Flask, request
import json
from jira.client import JIRA
from configuration import *
import urllib2

app = Flask(__name__)

def auth_jira_url(url):
    return url + "&os_username=" + JIRA_USERNAME + "&os_password=" + JIRA_PASSWORD

####################################################################
# Routes
####################################################################

@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')

@app.route('/jira/do_today', methods=['GET'])
def jira_do_today_count():
    return urllib2.urlopen(auth_jira_url(JIRA_BASE_URL + "/rest/api/2/search?jql=status=\"Do%20Today\"")).read()

####################################################################
# Start Flask
####################################################################
if __name__ == '__main__':
    app.run(debug=True)