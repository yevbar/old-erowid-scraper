import numpy as np
import pandas as pd

from gensim.models import Doc2Vec
from collections import namedtuple
import gensim.utils
import re
import string

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

model = Doc2Vec(dm=1, vector_size=300, window=10, hs=0, min_count=10, dbow_words=1, sample=1e-5)
model.build_vocab(alldocs)
EPOCHS = 100
for epoch in range(EPOCHS):
    model.train(alldocs, total_examples=model.corpus_count, start_alpha=0.01, end_alpha=0.01)
    print(epoch)
model.save("trip.model")
