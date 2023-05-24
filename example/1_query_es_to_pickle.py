"""
Example script to query from elasticsearch to get documents.
"""
import argparse
import pickle

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan


def main(args):
    client = Elasticsearch('https://ead-overseas-es.inner.youdao.com', http_auth=('', ''))
    # client = Elasticsearch()
    query = {
        "query": {
            "range": {
                "timestamp": {
                    "gte": "2023-01-01",
                    "lt": "2023-01-02",
                    "format": "yyyy-MM-dd",
                    "time_zone": "+08:00"
                }
            }
        }
    }

    data = []
    for i, hit in enumerate(scan(client, index="witake_media", query=query), start=1):
        data.append(hit)
        if i % 10000 == 0:
            print(i)
            # TODO
            # break

    with open(args.save, 'wb') as f:
        pickle.dump(data, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Indexing elasticsearch documents.')
    parser.add_argument('--save', default='example/data/data.bin', help='Elasticsearch documents.')
    args = parser.parse_args()
    main(args)
