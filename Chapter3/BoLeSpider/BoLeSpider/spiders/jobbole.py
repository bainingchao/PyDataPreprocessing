# -*- coding: utf-8 -*-
import scrapy,re



# 获取单页信息
'''
class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['http://www.jobbole.com/']
    start_urls = ['http://blog.jobbole.com/114638']

    # 获得单页的信息
    def parse(self, response):
        # css获取内容
        title = response.css('.entry-header h1::text').extract()   # 新闻题目
        crate_date = response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip().replace('·','')  # 创建时间
        url = response.url     # url
        dianzan = self.re_match(response.css('.vote-post-up h10::text').extract()[0]) # 点赞数
        soucang = self.re_match(response.css('.bookmark-btn::text').extract()[0]) # 收藏数
        comment = self.re_match(response.css('a[href="#article-comment"] span::text').extract()[0]) # 评论数

        print('标题:',title,'\n','发布时间:',crate_date,'\n','文章地址:',url,'\n','点赞数：',dianzan,'\n','收藏数',soucang,'\n','评论数',comment)


    # 对点赞数、收藏数、评论数等进行正则数字提取
    def re_match(self,value):
        match_value = re.match('.*?(\d+).*',value)
        if match_value:
            value = int(match_value.group(1))
        else:
            value = 0
        return value
'''


import datetime
from scrapy.http import Request
from urllib import parse
from BoLeSpider.items import JobBoleItem

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['http://www.jobbole.com/']
    # start_urls = ['http://blog.jobbole.com/114638']
    start_urls = ['http://blog.jobbole.com/all-posts/'] # 所有页信息


    # 获取列表下所有页信息
    def parse(self, response):
        # 1 获取文章列表中的具体文章url并交给解析函数具体字段解析
        post_urls = response.css("#archive .floated-thumb .post-thumb a::attr(href)").extract()
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url,post_url),callback=self.parses_detail, dont_filter=True) # scrapy下载

        #  2 提取下一页并交给scrapy提供下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse, dont_filter=True)

    # scrapy shell http://blog.jobbole.com/114638/
    def parses_detail(self, response):
        article_item =JobBoleItem()
        article_item['title'] = response.css('.entry-header h1::text').extract()
        article_item['create_date'] = date_convert(response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·","").strip())
        article_item['url'] = response.url
        article_item['dianzan'] = re_match(response.css('.vote-post-up h10::text').extract()[0])
        article_item['soucang'] = re_match(response.css('.bookmark-btn::text').extract()[0])
        article_item['comment'] = re_match(response.css('a[href="#article-comment"] span::text').extract()[0])
        yield article_item


# **************************正则对字段格式化处理******************************

# 对点赞数、收藏数、评论数等进行正则数字提取
def re_match(value):
    match_value = re.match('.*?(\d+).*',value)
    if match_value:
        nums = int(match_value.group(1))
    else:
        nums = 0
    return nums


# 对时间格式化处理
def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date