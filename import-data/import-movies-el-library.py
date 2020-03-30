import csv
from collections import deque
import elasticsearch
import re
from elasticsearch import helpers

def readMovies():
    csvfile= open('../ml-latest-small/movies.csv', 'r',encoding="utf8")
    reader = csv.DictReader( csvfile)
    for line in reader:
        movie = {}
        movie['movie_id'] = int(line['movieId'])
        title = line['title']
        title = re.sub(" \(.*\)$", "", re.sub('"','', title))
        movie['title'] = title
        year = movie['title'][-5:-1]
        movie['year'] = year
        genres = line['genres'].split('|')
        movie['genre'] = genres
        yield movie


es= elasticsearch.Elasticsearch()
es.indices.delete(index="movies",ignore=404)
deque(helpers.parallel_bulk(es,readMovies(),index="movies"), maxlen=0)
es.indices.refresh()
