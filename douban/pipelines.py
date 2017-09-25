#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json


class DoubanPipeline(object):
    # 初始化时指定要操作的文件
    def __init__(self):
        self.file = codecs.open('data.csv', 'wb', 'utf-8')

    # 存储数据，将 Item 实例作为 json 数据写入到文件中
    def process_item(self, item, spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + '\n'
       # print line + "+++++++dict+++++++++++++"
        #self.file.write(line.decode("unicode_escape"))
        self.file.write(lines)
        return item

    # 处理结束后关闭 文件 IO 流
    def close_spider(self, spider):
        self.file.close()
