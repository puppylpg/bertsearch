import os
from pprint import pprint

from flask import Flask, render_template, jsonify, request
from elasticsearch import Elasticsearch
import numpy as np
from pymilvus import (
    connections,
    Collection,
)
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

SEARCH_SIZE = 100
INDEX_NAME = os.getenv('INDEX_NAME', 'media_search')
app = Flask(__name__)


def normalize_vector(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


@app.route('/')
def index():
    return render_template('index.html')


client = Elasticsearch('elasticsearch:9200')


@app.route('/knn')
def knn():
    query = request.args.get('q')
    query_vector = normalize_vector(model.encode([query])[0].tolist())

    body = {
        "size": SEARCH_SIZE,
        "knn": {
            "field": "text_vector",
            "query_vector": query_vector,
            "k": SEARCH_SIZE,
            "num_candidates": SEARCH_SIZE + 100
        },
        "_source": {"includes": ["all", "title", "url"]}
    }

    response = client.search(
        index=INDEX_NAME,
        body=body,
        request_timeout=1000
    )
    pprint(query)
    # pprint(response)
    return jsonify(response)


@app.route('/search')
def search():
    query = request.args.get('q')

    match_query = {
        "match": {
            "all": query
        }
    }

    response = client.search(
        index=INDEX_NAME,
        body={
            "size": SEARCH_SIZE,
            "query": match_query,
            "_source": {"includes": ["all", "title", "url"]}
        }
    )
    pprint(query)
    # pprint(response)
    return jsonify(response)


connections.connect("default", host="milvus-standalone", port="19530")
collection_name = "media_search"
collection = Collection(collection_name)
collection.load()


@app.route('/milvus')
def milvus():
    query = request.args.get('q')
    query_vector = normalize_vector(model.encode([query])[0].tolist())

    search_params = {
        "metric_type": "IP",
        "params": {"ef": SEARCH_SIZE * 10}
    }

    result = collection.search(
        data=[query_vector],
        anns_field="text_vector",
        param=search_params,
        limit=SEARCH_SIZE,
        output_fields=['all', 'title', 'url']
    )

    result_dict = {}
    for hits in result:
        result_dict['hits'] = {}
        for hit in hits:
            if 'hits' not in result_dict['hits']:
                result_dict['hits']['hits'] = []
            result_dict['hits']['hits'].append({
                '_id': hit.id,
                '_score': hit.score,
                '_source': {
                    'all': hit.entity.get('all'),
                    'title': hit.entity.get('title'),
                    'url': hit.entity.get('url')
                }
            })

    # pprint(response)
    return result_dict


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
