import os
from pprint import pprint

import argparse
import json
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

SEARCH_SIZE = 10


def main(args):
    client = Elasticsearch('elasticsearch:9200')

    query = args.query
    query_vector = model.encode([query])[0].tolist()

    knn_query = {
        "knn": {
            "field": "text_vector",
            "query_vector": query_vector,
            "k": SEARCH_SIZE,
            "num_candidates": 1000
        }
    }

    body = {
        "size": SEARCH_SIZE,
        "query": knn_query,
        "_source": {"includes": ["title", "description", "tags"]}
    }
    print(json.dumps(body))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate elasticsearch query.')
    parser.add_argument('--query', default='hello world', help='Elasticsearch query content.')
    args = parser.parse_args()
    main(args)
