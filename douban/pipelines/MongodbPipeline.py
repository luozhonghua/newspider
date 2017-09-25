#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
from pymongo import MongoClient
''' 
DEBUG = True
if DEBUG:
    MONGODB_SERVER = "localhost"
    MONGODB_PORT = 27017
    MONGODB_DB = "douban_db"
    MONGODB_DOCNAME = "review_tb"
else:
    MONGODB_SERVER = "localhost"
    MONGODB_PORT = 27017
    MONGODB_DB = "douban_db"  #数据库名
    MONGODB_DOCNAME = "review_tb"  #表名
'''


class MongoDBPipeline(object):
    def __init__(self):
        host = settings['MONGODB_SERVER']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DB']
        #client = MongoClient(host,port)
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]
        print settings['MONGODB_DOCNAME']
    '''
   def process_item(self, item, spider):
       bookInfo = dict(item)
       self.post.insert(bookInfo)
       return item
    '''
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem('Missing{0}!'.format(data))
        if valid:
            #self.collection.insert(dict(item))
            self.post.insert(dict(item))
            log.msg('question added to mongodb database!',
                    level=log.DEBUG, spider=spider)
        return item
