# newspider
newspider is scrapy demo

please use ide of pycharm tool

项目简介
网络爬虫机器人，大数据前置技术，提供网络数据抓取和清洗，为大数据赋能
但是网络数据抓取的工作量大部分时间花费为各种网站的各种数据结构编写抓取、清洗规则及反爬虫对策上，因此后续版本将项目演进为网络爬虫框架，为开发用户赋能
项目技术栈
基于Scrapy框架，python描述，后续增加PhantomJS，Selenium
存储介质：文件格式，mysql格式，mongodb格式，elasticsearch格式


项目架构
单机架构

 



分布式架构(架构改进设想)
框架或项目参考
1、cola 
 


https://github.com/chineking/cola
https://github.com/chineking/cola/wiki（Chinese docs(wiki)）

Overview
Cola is a high-level distributed crawling framework, used to crawl pages and extract structured data from websites. It provides simple and fast yet flexible way to achieve your data acquisition objective. Users only need to write one piece of code which can run under both local and distributed mode



2、scrapy-redis
https://github.com/younghz/scrapy-redis/

Overview
his project attempts to provide Redis-backed components for Scrapy.

Features:
Distributed crawling/scraping
You can start multiple spider instances that share a single redis queue. Best suitable for broad multi-domain crawls.
Distributed post-processing
Scraped items gets pushed into a redis queued meaning that you can start as many as needed post-processing processes sharing the items queue.

Requirements:
Scrapy >= 0.14
redis-py (tested on 2.4.9)
redis server (tested on 2.4-2.6)

Available Scrapy components:
Scheduler
Duplication Filter
Item Pipeline
Base Spider







项目结构
 




实现功能
   抓取清洗music.douban.com下https://music.douban.com/subject/1406522/（一个或多个）列表所有的乐评详情数据，并同时存储MusicReviewItem_exporter.xml,mysql的review_tb表，mongodb的doubandb下的review_db, elasticsearch集群存储



 




抓取&清洗
web URL抓取分析
 

 


 




 

 



 






python
allowed_domains = ['music.douban.com']
start_urls = ['https://music.douban.com/subject/1406522/','https://music.douban.com/subject/26683363/','https://music.douban.com/subject/27146202/']
#start_urls = ['https://movie.douban.com/top250']
rules = (
    #乐评抓取规则定义
    Rule(LinkExtractor(allow=r"/subject/\d+/reviews$")),            #每个音乐的-乐评列表
    Rule(LinkExtractor(allow=r"/subject/\d+/reviews\?sort=time$")), #最新发布排序-乐评列表
    Rule(LinkExtractor(allow=r"/subject/\d+/reviews\?sort=time\&start=\d+$")),          #最新发布乐评列表page开始数字
    Rule(LinkExtractor(allow=r"/review/\d+/$"), callback="parse_review", follow=True),  #乐评  每条乐评详情


web page代码分析
要抓取的内容
 

 



 


 

 



python

def parse_review(self, response):
    try:
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




存储介质
 



运行效果

文件
 



mysql
 
select * from review_tb  where review_author like '识文煅字ok'
 




mongodb
 

db.getCollection('review_tb').find({"review_author":"识文煅字ok"})
 

质量&效率

硬件
10年旧笔记本电脑配置
 
 
 
网络
深圳AR会议室wify网速
 

数据

1、清洗后的数据大小(非压缩)

1.1、118条txt存储文件
 
1.2、118条mongodb存储文件
 


效率
Scrapy默认32并发数获取和清洗及存储后118条数据耗时5分钟

 
 



反反爬策略
反爬，是相对于网站方来说的，对方不想给你爬他站点的数据，所以进行了一些限制，这就是反爬。
反爬处理，是相对于爬虫方来说的，在对方进行了反爬策略之后，你还想爬相应的数据，就需要有相应的攻克手段，这个时候，就需要进行反爬处理。
事实上，反爬以及反爬处理都有一些基本的套路，万变不离其宗

常见的反爬主要策略：

IP限制
UA限制
Cookie限制
资源随机化存储
动态加载技术


对应反反爬处理主要手段：
IP代理池技术
用户代理池技术
Cookie保存与处理
自动触发技术
抓包分析技术+自动触发技术

反反爬借助工具
PhantomJS
Selenium



后续版本计划
1、优化架构Redis 共享URL  queue计划，实现分布式高性能一级域名爬取
2、增加反反爬虫设计，模拟登陆验证和反爬虫、反反爬手段等限制
3、增强动态api爬虫设计
4、大数据生态链基础数据构建
5、将爬虫能力api透明出来，提供运营跟运维
6、开源计划：将爬虫能力演进为框架产品，为开发用户赋能

参考资料
 1、  《Python数据处理》 杰奎琳•凯泽尔（Jacqueline，Kazil）凯瑟琳•贾缪尔（）凯瑟琳•贾缪尔（Katharine，Jarmul） 著；张亮，吕家明 译
购书地址：http://item.jd.com/12219342.html
2、 《精通Python网络爬虫：核心技术、框架与项目实战》   韦玮 著   
购书地址：http://item.jd.com/12056463.html?cpdad
3、  Scrapy+PhantomJS DEMO参考
https://segmentfault.com/a/1190000005866893
https://github.com/FullerHua/gooseeker


