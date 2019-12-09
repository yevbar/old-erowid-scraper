from flask import Flask, render_template, request, jsonify, send_file
from flask_pymongo import PyMongo
from collections import namedtuple
from gensim.models import Doc2Vec
import gensim.utils
import numpy as np
import pandas as pd
import re
import string
import time

app = Flask(__name__, template_folder="web/build", static_folder="web/build/static")
app.config["MONGO_URI"] = 'mongodb://heroku_rpsnn33f:3vm1tfdqreohngn2gorq70b9lp@ds219078.mlab.com:19078/heroku_rpsnn33f'
mongo = PyMongo(app)
model = Doc2Vec.load("trip.model")

@app.before_first_request
def setup():
    x = 1

@app.after_request
def add_header(response):
    response.cache_control.max_age = 300
    return response

@app.route("/")
def with_algolia():
    return send_file("./algolia.html")

@app.route("/doc2vec")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    start_time = time.time()
    request_json = request.json
    search_query = request_json["query"]
    results = search_for_trips(search_query)
    end_time = time.time()
    app.logger.critical("Time elapsed: {}".format(end_time-start_time))
    return jsonify({"data": results})

def search_for_trips(query):
    new_vector = model.infer_vector(query.split(), alpha=0.001, steps=5)
    sims = model.docvecs.most_similar([new_vector], topn=5)
    results = []
    for sim in sims:
        docsim = mongo.db.reports.find_one({"line_no": int(sim[0])})
        results.append({
            "report": docsim["report"],
            "title": docsim["title"],
            "substance": docsim["substance"]
        })
    return results

if __name__ == "__main__":
    app.run()
