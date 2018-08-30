import re
import os
from bs4 import BeautifulSoup
import scrapy
from scrapy.http import Request
from ..items import AppJuejinItem


class SpiderJuejin(scrapy.Spider):
    name = 'spider_juejin'
    allowed_domains = ['juejin.im']
    URL_JUEJIN = 'https://juejin.im/welcome/'
    OUTPUT_PATH = r'./../output/'
    JUEJIN_TABS = (
        'frontend'
        , 'android', 'ios'
        , 'backend'
        , 'design'
        , 'product'
        , 'freebie'
        , 'article'
        , 'ai'
        , 'devops')

    def start_requests(self):
        for tab in self.JUEJIN_TABS:
            url = f'{self.URL_JUEJIN}{tab}'
            yield Request(url, self.parse)

    def parse(self, response):
        print(response)
        articleList = BeautifulSoup(response.text, 'lxml').find_all('a', {'class': 'title'})
        with open('./output.txt', 'w', encoding='UTF-8') as f:
            for article in articleList:
                url = article.get('href')
                f.write(f'{article.string}\nhttps://juejin.im/{url}\n')

