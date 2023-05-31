"""
Example script to index elasticsearch documents.
"""
import argparse
import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def main(args):
    client = Elasticsearch('http://localhost:9200')
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
                bulk(client, data)
                data = []

        # 发送剩余的数据
        if data:
            bulk(client, data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Indexing elasticsearch documents.')
    parser.add_argument('--data', default='example/data/documents.jsonl', help='Elasticsearch documents.')
    args = parser.parse_args()
    main(args)
