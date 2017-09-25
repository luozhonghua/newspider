#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import treq
from twisted.internet import defer
from scrapy.exceptions import NotConfigured
from pyes import ES
import hashlib
from scrapy.utils.project import get_project_settings
from scrapy import log


class EsWriterPipeline(object):
    def __init__(self):
        self.settings = get_project_settings()
        basic_auth = {'username': self.settings['ELASTICSEARCH_USERNAME'],
                      'password': self.settings['ELASTICSEARCH_PASSWORD']}
        if self.settings['ELASTICSEARCH_PORT']:
            uri = "%s:%d" % (self.settings['ELASTICSEARCH_SERVER'], self.settings['ELASTICSEARCH_PORT'])
        else:
            uri = "%s" % (self.settings['ELASTICSEARCH_SERVER'])
        self.es = ES([uri], basic_auth=basic_auth)

    def process_item(self, item, spider):
        if self.__get_uniq_key() is None:
            log.msg("ELASTICSEARCH_UNIQ_KEY is NONE")
            self.es.index(dict(item), self.settings['ELASTICSEARCH_INDEX'], self.settings['ELASTICSEARCH_TYPE'],
                          id=item['id'], op_type='create', )
        else:
            self.es.index(dict(item), self.settings['ELASTICSEARCH_INDEX'], self.settings['ELASTICSEARCH_TYPE'],
                          self._get_item_key(item))
        log.msg("Item send to Elastic Search %s" %
                (self.settings['ELASTICSEARCH_INDEX']),
                level=log.DEBUG, spider=spider)
        return item

    def _get_item_key(self, item):
        uniq = self.__get_uniq_key()
        if isinstance(uniq, list):
            values = [item[key] for key in uniq]
            value = ''.join(values)
        else:
            value = uniq
        return hashlib.sha1(value).hexdigest()

    def __get_uniq_key(self):
        if not self.settings['ELASTICSEARCH_UNIQ_KEY'] or self.settings['ELASTICSEARCH_UNIQ_KEY'] == "":
            return None
        return self.settings['ELASTICSEARCH_UNIQ_KEY']

    ''' 
        """A pipeline that writes to Elastic Search"""
        @classmethod
        def from_crawler(cls, crawler):
            """Create a new instance and pass it ES's url"""

            # Get Elastic Search URL
            es_url = crawler.settings.get('ES_PIPELINE_URL', None)

            # If doesn't exist, disable
            if not es_url:
                raise NotConfigured

            return cls(es_url)

        def __init__(self, es_url):
            """Store url and initialize error reporting"""

            # Store the url for future reference
            self.es_url = es_url

        @defer.inlineCallbacks
        def process_item(self, item, spider):
            """
            Pipeline's main method. Uses inlineCallbacks to do
            asynchronous REST requests
            """
            try:
                # Create a json representation of this item
                data = json.dumps(dict(item), ensure_ascii=False).encode("utf-8")
                print ">>>>>>>>>>>>> "+data
                yield treq.post(self.es_url, data, timeout=5)
            finally:
                # In any case, return the dict for the next stage
                defer.returnValue(item)
           '''
