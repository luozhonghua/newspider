#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
from douban.items import MusicItem, MusicReviewItem, MusicCommentsItem

DEBUG = True

if DEBUG:
    dbuser = 'root'
    dbpass = 'root'
    dbname = 'database'
    dbhost = '127.0.0.1'
    dbport = '3306'
else:
    dbuser = 'root'
    dbpass = 'root'
    dbname = 'database'
    dbhost = '127.0.0.1'
    dbport = '3306'


class MySQLStorePipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user=dbuser, passwd=dbpass, db=dbname, host=dbhost, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()
        # 建立需要存储数据的表

        # 清空表（测试阶段）：
        self.cursor.execute("truncate table music_tb;")
        self.conn.commit()
        self.cursor.execute("truncate table review_tb;")
        self.conn.commit()
        self.cursor.execute("truncate table comments_tb;")
        self.conn.commit()

    def process_item(self, item, spider):

        if isinstance(item, MusicItem):
            print "开始写入音乐信息"
            try:
                self.cursor.execute("""INSERT INTO music_tb (music_name, music_alias, music_singer, music_rating, music_votes, music_tags,music_url)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                                    (
                                        # item['_id'].encode('utf-8'),
                                        item['music_name'].encode('utf-8'),
                                        item['music_alias'].encode('utf-8'),
                                        item['music_singer'].encode('utf-8'),
                                        item['music_rating'].encode('utf-8'),
                                        item['music_votes'].encode('utf-8'),
                                        item['music_tags'].encode('utf-8'),
                                        item['music_url'].encode('utf-8'),
                                    )
                                    )

                self.conn.commit()
            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])

        elif isinstance(item, MusicReviewItem):
            print "开始写入乐评信息"
            # item['Pic_Url'].encode('utf-8')
            try:
                self.cursor.execute("""INSERT INTO review_tb (review_title, review_content, review_author, review_music, review_time, review_url)
                                VALUES (%s, %s, %s, %s, %s, %s)""",
                                    (
                                        # 在parse2中除了_id其他返回的都是列表，需要提取第一个元素
                                        # item['_id'].encode('utf-8'),
                                        item['review_title'].encode('utf-8'),
                                        item['review_content'].encode('utf-8'),
                                        item['review_author'].encode('utf-8'),
                                        item['review_music'].encode('utf-8'),
                                        item['review_time'].encode('utf-8'),
                                        item['review_url'].encode('utf-8')
                                    )
                                    )
                self.conn.commit()
            except MySQLdb.Error, e:
                print "出现错误"
                print "Error %d: %s" % (e.args[0], e.args[1])


        elif isinstance(item, MusicCommentsItem):
            print "开始写入短评信息"
            try:
                self.cursor.execute("""INSERT INTO review_tb (comments_author, comments_content, comments_time)
                                    VALUES (%s, %s, %s)""",
                                    (
                                        # 在parse2中除了_id其他返回的都是列表，需要提取第一个元素
                                        item['comments_author'].encode('utf-8'),
                                        item['comments_content'].encode('utf-8'),
                                        item['comments_time'].encode('utf-8')
                                    )
                                    )
                self.conn.commit()
            except MySQLdb.Error, e:
                print "出现错误"
                print "Error %d: %s" % (e.args[0], e.args[1])

        return item
