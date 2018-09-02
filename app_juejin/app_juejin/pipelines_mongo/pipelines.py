import pymongo
from scrapy.conf import settings


class MongoPipeline(object):
    name = 'MongoPipeline'
    collection = 'juejinarticles'

    def __init__(self):
        self.mongo_uri = settings["MONGO_URL"]
        self.mongo_dbname = settings["MONGO_DBNAME"]

    def open_spider(self, spider):
        # spider start
        print('self.mongo_uri', self.mongo_uri)
        print('self.mongo_dbname', self.mongo_dbname)
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_dbname]
        pass

    def close_spider(self, spider):
        # spider stop
        self.client.close()

    def process_item(self, item, spider):
        if not item['title']:
            return item
        data = {
            'title': item['title'],
            'type': item['type'],
            'url': item['url'],
            'html': item['html']
        }
        table = self.db[self.collection]
        table.insert_one(data)
        print('[INFO] save item successfully!')
        return item
