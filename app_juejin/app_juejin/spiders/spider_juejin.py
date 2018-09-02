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
        , 'devops'
    )

    def start_requests(self):
        for tab in self.JUEJIN_TABS:
            url = f'{self.JUEJIN_URL}{tab}'
            yield Request(url, self.parse, meta={'tab': tab})

    def parse(self, response):
        # self.grep_article_info_and_save_files(response)
        return self.grep_article_detail_and_parse_to_item(response)

    def grep_article_info_and_save_files(self, response):
        file_name = response.meta['tab']
        print('tab => ', file_name)
        article_list = BeautifulSoup(response.text, 'lxml').find_all('a', {'class': 'title'})
        if not os.path.exists(self.OUTPUT_PATH):
            os.mkdir(self.OUTPUT_PATH)
        self.save_article_list_to_files(article_list, file_name)

    def grep_article_detail_and_parse_to_item(self, response):
        tab = response.meta['tab']
        article_list = BeautifulSoup(response.text, 'lxml').find_all('a', {'class': 'title'})
        for article in article_list:
            title = article.string
            url = article.get('href')
            url = f'{self.JUEJIN_HOST}{url}'
            print('[INFO] Start request url:', url)
            params = {'meta': {'title': title, 'url': url, 'tab': tab}}
            # yield self.parse_article_detail_item(params)
            yield Request(url, callback=self.parse_article_detail_item, meta={'title': title, 'url': url, 'tab': tab})

    def save_article_list_to_files(self, article_list, file_name):
        with open(f'{self.OUTPUT_PATH}{file_name}.txt', 'w', encoding='UTF-8') as f:
            for article in article_list:
                url = article.get('href')
                f.write(f'{article.string}\n{self.JUEJIN_HOST}{url}\n')

    def parse_article_detail_item(self, response):
        item = AppJuejinCrticleItem()
        item['title'] = response.meta['title']
        item['url'] = response.meta['url']
        item['type'] = response.meta['tab']
        item['html'] = response.body
        print('[INFO] [parseArticleDetailItem] item create finish!', item['title'], item['url'], item['type'])
        return item
