import argparse

import numpy as np
from pymilvus import (
    connections,
    Collection,
)
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

SEARCH_SIZE = 10

connections.connect("default", host="localhost", port="19530")
collection_name = "media_search"
collection = Collection(collection_name)
# collection.load()


def normalize_vector(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def main(args):
    query = args.query
    v = model.encode([query])
    query_vector = normalize_vector(v[0].tolist())

    # print(f'query_vector shape: {query_vector.shape}')

    search_params = {
        "metric_type": "IP",
        "params": {"ef": SEARCH_SIZE * 10}
    }

    result = collection.search(
        data=[query_vector],
        anns_field="text_vector",
        param=search_params,
        limit=SEARCH_SIZE,
        output_fields=['all']
    )

    for hits in result:
        for hit in hits:
            print(f"_id: {hit.id}")
            print(f"hit: {hit}, field: {hit.entity.get('all')}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate elasticsearch query.')
    parser.add_argument('--query', default='hello world', help='Elasticsearch query content.')
    args = parser.parse_args()
    main(args)
