
- mkdir example/data
- 从es获取大约60w个media需要3min【这里必须使用elasticsearch==7.12.0，不能使用8】；
- 在笔记本上，向量化1w个media用了21min，60w个预计20h+；zj068上8h；th140上5.5h;
- index进elasticsearch大约1min。

注意事项：
- 使用docker-compose启动之前需要设置`export INDEX_NAME=media_search`
- example/data别忘了创建
- example可能需要`conda install scikit-learn`，pip不知道为啥没成功

