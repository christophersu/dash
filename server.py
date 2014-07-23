#!/usr/bin/env python
from flask import Flask, render_template, jsonify, request
from configuration import *

app = Flask(__name__)

####################################################################
# Routes
####################################################################

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', header='Flask Skeleton', title='Flask Skeleton', body='''
        <p>Some content can go here!</p>
        ''')

####################################################################
# Start Flask
####################################################################
if __name__ == '__main__':
    app.run(debug=True)