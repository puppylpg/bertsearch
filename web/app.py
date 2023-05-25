import os
from pprint import pprint

from flask import Flask, render_template, jsonify, request
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

SEARCH_SIZE = 100
INDEX_NAME = os.environ['INDEX_NAME']
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def analyzer():
    client = Elasticsearch('elasticsearch:9200')

    query = request.args.get('q')
    query_vector = model.encode([query])[0].tolist()

    body = {
        "size": SEARCH_SIZE,
        "knn": {
            "field": "text_vector",
            "query_vector": query_vector,
            "k": SEARCH_SIZE,
            "num_candidates": SEARCH_SIZE + 100
        },
        "_source": {"includes": ["all", "title"]}
    }

    response = client.search(
        index=INDEX_NAME,
        body=body
    )
    print(query)
    # pprint(response)
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
