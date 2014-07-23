#!/usr/bin/env python
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from configuration import *

app = Flask(__name__)

# ###################################################################
# Check if running locally on on Heroku and setup MongoDB accordingly
# ###################################################################
on_heroku = False
if 'MONGOLAB_URI' in os.environ:
  on_heroku = True

if on_heroku:
    client = MongoClient(os.environ['MONGOLAB_URI'])
    db = client.get_default_database()
    collection = db.data
else:
    client = MongoClient('mongodb://localhost:27017/')
    db = client.instachart
    collection = db.data

# ###################################################################
# Routes
# ###################################################################

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', header='Flask Skeleton', title='Flask Skeleton', body='''
        <p>Some content can go here!</p>
        ''')

# ###################################################################
# Start Flask
# ###################################################################

if __name__ == '__main__':
    app.run(debug=True)