
import sqlite3
from flask import Flask, render_template, send_from_directory, request
import sys

sys.path.append('..')

import main

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return send_from_directory('client/public', 'index.html')

@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

@app.route("/api/getmatrix", methods = ['POST'])
def getmatrix():
    voters = request.json["voters"]
    proposals = request.json["proposals"]
    problem_statement = """We are choosing which proposals to allocate funding to."""
    user_inputs = [voter["preferences"] for voter in voters]
    options = ['A proposed course of action: ```' + proposal["description"] + '``` with a predited outcome of: ```' + proposal["outcome"] + '```' for proposal in proposals]
    res = main.simple_voting(problem_statement, user_inputs, options)
    return res


if __name__ == '__main__':
    app.run(debug=True)
