import os
from bs4 import BeautifulSoup
import scrapy
from scrapy.http import Request
from ..items import AppJuejinItem, AppJuejinCrticleItem


class SpiderJuejin(scrapy.Spider):
    name = 'spider_juejin'
    allowed_domains = ['juejin.im']
    JUEJIN_HOST = 'https://juejin.im'
    JUEJIN_URL = 'https://juejin.im/welcome/'
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
            url = f'{self.}{tab}'
            yield Request(url, self.parse, meta={'tab': tab})

    def parse(self, response):
        self.grepCirticleInfoAndSaveFiles(response)

    def grepCirticleInfoAndSaveFiles(self, response):
        fileName = response.meta['tab']
        print('tab => ', fileName)
        articleList = BeautifulSoup(response.text, 'lxml').find_all('a', {'class': 'title'})

        if not os.path.exists(self.OUTPUT_PATH):
            os.mkdir(self.OUTPUT_PATH)

        self.saveArticleList(articleList)

        for article in articleList:
            title = article.string
            url = article.get('href')
            url = f'{self.JUEJIN_HOST}{url}'
            yield Request(url, callback=self.parseArticleDetailItem, meta={'title': title, 'url': url})

    def saveArticleList(self, articleList):
        with open(f'{self.OUTPUT_PATH}{fileName}.txt', 'w', encoding='UTF-8') as f:
            for article in articleList:
                url = article.get('href')
                f.write(f'{article.string}\n{self.JUEJIN_HOST}{url}\n')

    def parseArticleDetailItem(self, response):
        item = AppJuejinCrticleItem
        item.title = response.meta['title']
        item.url = response.meta['url']
        item.html = BeautifulSoup(response.txt, 'lxml').find_all('.article')[0].get_text()
        return item
