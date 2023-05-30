"""
Example script to index elasticsearch documents.
"""
import argparse
import json

import numpy as np
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)

collection_name = "media_search"


def normalize_vector(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def bulk(collection, docs):
    entities = [
        [doc['_id'] for doc in docs],
        [doc.get('title', '') for doc in docs],
        [doc.get('description', '') for doc in docs],
        [doc.get('tags', '') for doc in docs],
        [doc.get('all', '') for doc in docs],
        [doc.get('url', '') for doc in docs],
        [doc.get('platform', '') for doc in docs],
        # 单位向量
        [normalize_vector(doc.get('text_vector', '')) for doc in docs]
    ]
    result = collection.insert(entities)
    return result


def main(args):
    connections.connect("default", host="localhost", port="19530")

    has = utility.has_collection(collection_name)
    print(f"Does collection {collection_name} exist in Milvus: {has}")

    if has:
        utility.drop_collection(collection_name)
        print(f"Delete collection {collection_name} successfully")

    fields = [
        FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
        FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=1000),
        FieldSchema(name="description", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="tags", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="all", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="url", dtype=DataType.VARCHAR, max_length=200),
        FieldSchema(name="platform", dtype=DataType.VARCHAR, max_length=20),
        FieldSchema(name="text_vector", dtype=DataType.FLOAT_VECTOR, dim=768)
    ]

    schema = CollectionSchema(fields, "media_search in milvus")

    collection = Collection(collection_name, schema, consistency_level="Strong")

    with open(args.data, 'r') as f:
        # 初始化计数器和数据列表
        count = 0
        data = []

        # 逐行读取文件内容
        for line in f:
            # 反序列化为 JSON 对象
            json_obj = json.loads(line.strip())

            # 将 JSON 对象添加到数据列表中
            data.append(json_obj)

            # 每 1000 行发送一次请求
            count += 1
            if count % 1000 == 0:
                print(count)
                bulk(collection, data)
                data = []

        # 发送剩余的数据
        if data:
            bulk(collection, data)

    collection.flush()
    print(f"Number of entities in Milvus: {collection.num_entities}")

    index = {
        "index_type": "HNSW",
        "metric_type": "IP",
        "params": {
            'M': 30,
            'efConstruction': 200
        }
    }

    collection.create_index("text_vector", index)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Indexing elasticsearch documents.')
    parser.add_argument('--data', default='example/data/documents.jsonl', help='Elasticsearch documents.')
    args = parser.parse_args()
    main(args)
