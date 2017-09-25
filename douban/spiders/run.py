#!/usr/bin/python
# -*- coding: UTF-8 -*-
from scrapy import cmdline
#from douban.utils import Py2utils
import sys
#修改默认系统编码
#reload(sys)
#sys.setdefaultencoding('utf-8')

str1 = '\u4e1c\u98ce\u7834\u662f\u5468\u6770\u4f26\u4e00\u751f\u6240\u7cfb\u6700\u597d\u7684\u7684\u4e00\u9996\u6b4c'
str2='\xe9\x83\x81\xe7\xa8\x8b'
#print str2
#print type(str1)
#print sys.getdefaultencoding()
#print str1.decode('unicode_escape')
#print str1.decode('gbk').encode('utf-8')
#print str1.decode('gbk')

#注意每种格式都有不同的编码，要做成一个通用编码库
#'xml', 'jsonlines', 'jl', 'json', 'csv', 'pickle', 'marshal
#cmdline.execute("scrapy crawl review -o review.xml".split())
cmdline.execute("scrapy crawl review".split())
