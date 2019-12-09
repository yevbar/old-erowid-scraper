from collections import namedtuple
from gensim.models import Doc2Vec
import gensim.utils
import numpy as np
import pandas as pd
import re
import string

model = Doc2Vec.load("trip.model")
trip_data = pd.read_csv("trips.csv")
data = np.array(trip_data.report)
titles = np.array(trip_data.title)
substances = np.array(trip_data.substance)

SentimentDocument = namedtuple("SentimentDocument", "words tags title substance original_number")
n = 0
alldocs = []

regex = re.compile('[%s]' % re.escape(string.punctuation))

for line_no, line in enumerate(data):
    if type(line) is str:
        line = regex.sub('', line)
        tokens = gensim.utils.to_unicode(line).lower().split()
        words = tokens[0:]
        tags = [n]
        title = titles[line_no]
        substance = substances[line_no]
        alldocs.append(SentimentDocument(words, tags, title, substance, line_no))
        n += 1

tokens = "happy"

new_vector = model.infer_vector(tokens.split(), alpha=0.001, steps=5)
tagssim = model.docvecs.most_similar([new_vector])[0]

docsim = alldocs[tagssim[0]]

new_vector = model.infer_vector(tokens.split() ,alpha=0.001 ,steps = 5)
tagsim = model.docvecs.most_similar([new_vector])[0]

# docsim = alldocs[tagsim[0]]

# print(docsim.original_number)
# print("Document:", data[docsim.original_number], "\n")
# print("Title:", docsim.title)
# print("Substance:", docsim.substance)

sims = model.docvecs.most_similar([new_vector], topn=5)
for sim in sims:
    docsim = alldocs[sim[0]]
    print("Document:", data[docsim.original_number], "\n")
    print("Title:", docsim.title)
    print("Substance:", docsim.substance)
