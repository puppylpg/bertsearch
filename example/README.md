# 数据准备
在工程根目录下：
1. `mkdir example/data`
2. 安装依赖。`pip install -r example/requirements.txt`。python elasticsearch 8不能查询线上7.12.0，所以需要把文件里的es版本改为7.12.0
3. 从es获取media数据，用作demo数据：`python example/1_query_es_to_pickle.py`。生成`example/data/data.bin`。可以修改查询的时间范围以控制media数量；
4. 对文本进行向量编码：`python example/2_create_documents_from_pickle.py`。生成`example/data/documents.jsonl`

一些简单的时间预估：
- 从es获取大约60w个media需要3min【这里必须使用elasticsearch==7.12.0，不能使用8】；
- 向量编码： 
  - 在笔记本上，向量化1w个media用了21min，60w个预计20h+；
  - zj068上8h；
  - th140上5.5h;
  - gpu246上一张卡编码60w大约20min；
- 把编码后的数据index进elasticsearch也比较快。

# 启动服务
在工程根目录下：需要ticket申请docker权限（`docker version`是否报错），使用`pip install docker-compose`安装docker-compose。
1. `docker-compose up`，服务陆续启动，web会挂掉，因为milvus里没有索引media_search，不重要；

`docker-compose.yaml`里es的heap设置的2G，太小了，可以考虑改成8G，甚至更大。

# 数据摄入
在工程根目录下：
1. 创建es索引：`python example/0_create_index.py`
2. es数据摄入：`python example/3_index_documents.py`
3. milvus索引创建、数据摄入：`python example/3_milvus_index_documents.py`

注意：实际使用时发现在gpu246上使用docker-compose启动的上述服务，有时候无法在gpu246上访问服务，但是可以在其他任意机器上使用`gpu246:<port>`访问相应服务（很迷……）。如果遇到上述问题，可以在其他机器（比如th077）上执行上述索引创建、数据摄入的任务。执行前记得把python程序里elasticsearch/milvus client所连接的地址设置为`gpu246:<port>`。

# 重启服务
在工程根目录下：
1. `docker-compose down`
2. `docker-compose up`

# 访问服务
- localhost:5000

辅助数据查看：
- kibana查看es数据: localhost:5601
- attu查看milvus数据: localhost:8000


其他注意事项：
- 安装example的依赖时在有的机器上没有安装成功，可能需要再手动执行一下`conda install scikit-learn`。

