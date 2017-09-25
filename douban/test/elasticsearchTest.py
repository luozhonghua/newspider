#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import datetime
from elasticsearch import Elasticsearch

import jpype
#调用java
jvmPath = jpype.getDefaultJVMPath()
jpype.startJVM(jvmPath)
jpype.java.lang.System.out.println("hello world!")
jpype.shutdownJVM()


# 连接elasticsearch,默认是9200
es = Elasticsearch("192.168.1.103:9201")
#es = Elasticsearch([{'host':'192.168.176.135','port':9200},{'host':'192.168.176.136','port':9200}])

# 插入数据,(这里省略插入其他两条数据，后面用)
#es.index(index="my-index", doc_type="test-type", id=01, body={"any": "data01", "timestamp": datetime.now()})
# {u'_type':u'test-type',u'created':True,u'_shards':{u'successful':1,u'failed':0,u'total':2},u'_version':1,u'_index':u'my-index',u'_id':u'1}
# 也可以，在插入数据的时候再创建索引test-index
es.index(index="test-index", doc_type="test-type", id=42, body={"any": "data", "timestamp": datetime.now()})

# 查询数据，两种get and search
# get获取
res = es.get(index="my-index", doc_type="test-type", id=01)
print(res)
# {u'_type': u'test-type', u'_source': {u'timestamp': u'2016-01-20T10:53:36.997000', u'any': u'data01'}, u'_index': u'my-index', u'_version': 1, u'found': True, u'_id': u'1'}
print(res['_source'])
# {u'timestamp': u'2016-01-20T10:53:36.997000', u'any': u'data01'}
