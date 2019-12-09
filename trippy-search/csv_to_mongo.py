import numpy as np
import pandas as pd
from pymongo import MongoClient
connection = MongoClient('mongodb://heroku_rpsnn33f:3vm1tfdqreohngn2gorq70b9lp@ds219078.mlab.com:19078/heroku_rpsnn33f?retryWrites=false')
db = connection["heroku_rpsnn33f"]
result = db.reports.find_one({})

trip_data = pd.read_csv("trips.csv")
data = np.array(trip_data.report)

for line_no, line in enumerate(data):
    if type(line) is str:
        db.reports.update_one({"line_no": line_no}, {"$set": {"report": line}})
