"""
Example script to create elasticsearch documents.
"""
import argparse
import json
import pickle
import numpy as np
import os
import torch

from sentence_transformers import SentenceTransformer

# 设置CUDA_VISIBLE_DEVICES环境变量
os.environ['CUDA_VISIBLE_DEVICES'] = '2,3'
print(f'gpu available? #{torch.cuda.is_available()}')
print(f'gpu count? #{torch.cuda.device_count()}')
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')


def normalize_vector(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def create_document(doc, emb, index_name):
    return {
        '_op_type': 'index',
        '_index': index_name,
        '_id': doc['_id'],
        '_routing': doc['_routing'],
        'title': doc['_source'].get('title', ''),
        'description': doc['_source'].get('description', ''),
        'tags': doc['_source'].get('tags', ''),
        'all': '\n'.join([doc['_source'].get('title', ''), doc['_source'].get('description', ''), doc['_source'].get('tags', '')]),
        'text_vector': emb,
        'platform': doc['_source'].get('platform', ''),
        'url': doc['_source'].get('url', '')
    }


def load_dataset(path):
    # 从文件中读取序列化的对象
    with open(path, "rb") as f:
        deserialized = pickle.load(f)
    return deserialized


def bulk_predict(docs, batch_size=256):
    """Predict bert embeddings."""
    for i in range(0, len(docs), batch_size):
        print(i)
        batch_docs = docs[i: i+batch_size]
        texts = []
        for doc in batch_docs:
            text = '\n'.join([doc['_source'].get('title', ''), doc['_source'].get('description', ''), doc['_source'].get('tags', '')])
            texts.append(text)
        embeddings = model.encode(texts)
        for emb in embeddings:
            yield normalize_vector(emb).tolist()


def main(args):
    docs = load_dataset(args.data)
    with open(args.save, 'w', encoding='utf8') as f:
        for doc, emb in zip(docs, bulk_predict(docs)):
            d = create_document(doc, emb, args.index_name)
            f.write(json.dumps(d) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creating elasticsearch documents.')
    parser.add_argument('--data', default='example/data/data.bin', help='data for creating documents.')
    parser.add_argument('--save', default='example/data/documents.jsonl', help='created documents.')
    parser.add_argument('--index_name', default='media_search', help='Elasticsearch index name.')
    args = parser.parse_args()
    main(args)
