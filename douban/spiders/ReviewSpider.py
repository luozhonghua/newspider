#!/usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from douban.items import MusicItem, MusicReviewItem,MusicCommentsItem
from scrapy import log
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
import urlparse
import re
from douban.utils import Py2utils
import sys
from scrapy.selector import Selector
from scrapy.http import Request
#修改默认系统编码
reload(sys)
sys.setdefaultencoding('utf-8')

class ReviewSpider(CrawlSpider):
    name = 'review'
    allowed_domains = ['music.douban.com']
    start_urls = ['https://music.douban.com/subject/1406522/']
    #start_urls = ['https://movie.douban.com/top250']
    rules = (
        #乐评抓取规则定义
        Rule(LinkExtractor(allow=r"/subject/\d+/reviews$")),            #每个音乐的-乐评列表
        Rule(LinkExtractor(allow=r"/subject/\d+/reviews\?sort=time$")), #最新发布排序-乐评列表
        Rule(LinkExtractor(allow=r"/subject/\d+/reviews\?sort=time\&start=\d+$")),          #最新发布乐评列表page开始数字
        Rule(LinkExtractor(allow=r"/review/\d+/$"), callback="parse_review", follow=True),  #乐评  每条乐评详情

        #短评抓取规则定义
        #Rule(LinkExtractor(allow=r"/subject/\d+/comments$")),  # 每个音乐的-短评列表
        #Rule(LinkExtractor(allow=r"/subject/\d+/comments/new$")), #最新发布排序-短评列表
        #Rule(LinkExtractor(allow=r"/subject/\d+/comments/new\?p=\d+$")),  # 最新发布排序-短评列表page开始数字
        #Rule(LinkExtractor(allow=r"/people/\d+/$"), callback="parse_comments", follow=True),
    )

    ''' 
    headler = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }

   
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headler)

    def parse(self, response):
        for quote in response.css('div.item'):
            yield {
                "电影名": quote.css('div.info div.hd a span.title::text').extract_first(),
                "评分": quote.css('div.info div.bd div.star span.rating_num::text').extract(),
                "引言": quote.css('div.info div.bd p.quote span.inq::text').extract()
            }
        next_url = response.css('div.paginator span.next a::attr(href)').extract()
        if next_url:
            next_url = "https://movie.douban.com/top250" + next_url[0]
            print(next_url)
            yield scrapy.Request(next_url, headers=self.headler)
      '''

    '''
    url = 'http://movie.douban.com/top250'
    def parse(self, response):
        # print response.body
        item = MusicCommentsItem()
        selector = Selector(response)
        Movies = selector.xpath('//div[@class="info"]')
        for eachMoive in Movies:
            title = eachMoive.xpath('div[@class="hd"]/a/span/text()').extract()
            fullTitle = ''
            for each in title:
                fullTitle += each
            movieInfo = eachMoive.xpath('div[@class="bd"]/p/text()').extract()
            star = eachMoive.xpath('div[@class="bd"]/div[@class="star"]/span[1]/text()').extract()[0]
            quote = eachMoive.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            # quote可能为空，因此需要先进行判断
            if quote:
                quote = quote[0]
            else:
                quote = ''
            #item['title'] = fullTitle
            #item['movieInfo'] = ';'.join(movieInfo)
            item['star'] = star
            item['quote'] = quote
            item['comments_content'] = ';'.join(movieInfo)
            yield item
        nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()
        print nextLink
        # 第10页是最后一页，没有下一页的链接
        if nextLink:
            nextLink = nextLink[0]
            print nextLink
            yield Request(self.url + nextLink, callback=self.parse)

      '''



    #############################
    def parse_comments(self, response):
        try:
            item = MusicCommentsItem()
            content = "".join(response.xpath('//*[@class="comment"]/div[@class="comment-report"]/text()').extract())  #详情页  property="v:description" 文本
            item['comments_content'] = content.lstrip().rstrip().replace("\n", " ")
            print content.lstrip().rstrip().replace("\n", " ")
            item['comments_author'] = "".join(response.xpath('//*[@class = "comment-info"]/a[1]/text()').extract()[0])   #详情页span property="v:reviewer"  文本
            item['comments_time'] = "".join(response.xpath('//*[@class="comment-info"]/span[2]/text()').extract())        #详情页class="main-hd" 第三个span  文本
            print response.url
            yield item
        except Exception as error:
            log(error)

    def parse_review(self, response):
        try:
            '''
            # Create the loader using the response
            l = ItemLoader(item=MusicReviewItem(), response=response)
            # Load fields using XPath expressions
            l.add_xpath('review_title', '//*[@property="v:summary"]/text()')
            content = "".join( response.xpath('//*[@id="link-report"]/div[@property="v:description"]/text()').extract()).lstrip().rstrip().replace("\n", " ")
            l.add_xpath('review_content', content)
            l.add_xpath('review_author', '//*[@property = "v:reviewer"]/text()')
            l.add_xpath('review_music', '//*[@class="main-hd"]/a[2]/text()')
            l.add_xpath('review_time', '//*[@class="main-hd"]/p/text()')
            l.add_xpath('review_url', response.url)
            yield l.load_item()
            '''
            item = MusicReviewItem()
            item['review_title'] = "".join(response.xpath('//*[@property="v:summary"]/text()').extract())                #详情页 property="v:summary"      文本
            content = "".join(response.xpath('//*[@id="link-report"]/div[@property="v:description"]/text()').extract())  #详情页  property="v:description" 文本
            item['review_content'] = content.lstrip().rstrip().replace("\n", " ")
            item['review_author'] = "".join(response.xpath('//*[@property = "v:reviewer"]/text()').extract()[0])   #详情页span property="v:reviewer"  文本
            item['review_music'] = "".join(response.xpath('//*[@class="main-hd"]/a[2]/text()').extract())          #详情页class="main-hd" 第二个a     文本
            item['review_time'] = "".join(response.xpath('//*[@class="main-hd"]/span[3]/text()').extract())        #详情页class="main-hd" 第三个span  文本
            item['review_url'] = response.url
            yield item
        except Exception as error:
            log(error)

