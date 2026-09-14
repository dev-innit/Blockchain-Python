from flask import Flask
from flask import request

node = Flask(__name__)

# store transcations in a list
this_transcations = []

@node.route('/transcations/new', methods=['POST'])